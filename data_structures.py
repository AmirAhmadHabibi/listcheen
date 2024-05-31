# This code is only for algorithmic porpuses and it's by no means optimized!

import itertools


def file2list(path) -> list:
    with open(path, "r", encoding="utf-8") as inf:
        file_list = list(line.strip() for line in inf)
    return file_list


FIELDS_OF_STUDY = file2list("./initial_data/daftarcheh/fields_of_study.txt")
UNIVERSITIES = file2list("./initial_data/daftarcheh/universities.txt")
PROGRAM_TYPES = file2list("./initial_data/daftarcheh/program_types.txt")

# fill this with triples of almost all combinations of the above (based on the دفترچه انتخاب رشته)
#           OPTIONS = [(FIELDS_OF_STUDY[0], UNIVERSITIES[0], PROGRAM_TYPE[0]), ...]
OPTIONS = list(itertools.product(*[FIELDS_OF_STUDY, UNIVERSITIES, PROGRAM_TYPES]))

CRITERION_CATEGORIES = {
    "FIELD_OF_STUDY": FIELDS_OF_STUDY,
    "UNIVERSITY": UNIVERSITIES,
    "PROGRAM_TYPE": PROGRAM_TYPES,
}  # indicating the part of the subject a criterion


# There are two main group of numbers that we are to figure out:
#  (1) criterion weight
#  (2) criterion value for each of its subject values (i.e. each university if the subject is 'U)
class Criterion:
    def __init__(
        self,
        name: str,
        category2weight: dict,
        default_value: float,
        different_for_each_option: bool,
        is_constant_value: bool,
    ) -> None:

        self.name = name
        self.category2weight = category2weight
        self.different_for_each_option = (
            different_for_each_option  # if multicat then diffetent for each option
        )
        self.is_constant_value = is_constant_value

        if different_for_each_option:
            value_rows = OPTIONS
        elif len(category2weight) == 1:
            # there can only be one category
            cat = list(category2weight.keys())[0]
            value_rows = CRITERION_CATEGORIES[cat]
        else:
            raise Exception("shouldn't have more than 1 category!")

        self.values = {
            s: default_value for s in value_rows
        }  # all valued from 0.0 to 1.0

    def get_score(self, option: tuple, weighted=True, cat=None) -> float:
        score = 0.0
        if self.different_for_each_option:
            score = self.values[option]
        elif len(self.category2weight) == 1:
            cat = list(self.category2weight.keys())[0]
            if cat == "FIELD_OF_STUDY":
                score = self.values[option[0]]
            elif cat == "UNIVERSITY":
                score = self.values[option[1]]
            elif cat == "PROGRAM_TYPE":
                score = self.values[option[2]]
            else:
                raise Exception("what?!")

        else:
            raise Exception("shouldn't have more than 1 category!")

        if weighted:
            return self.category2weight[cat] * score
        else:
            return score

    def __getitem__(self, key: str) -> float:
        return self.values[key]

    def __setitem__(self, key: str, val: float) -> None:
        if val < 0.0 or val > 1.0:
            raise ValueError("Value should be in range of 0.0 t0 1.0")
        self.values[key] = val
