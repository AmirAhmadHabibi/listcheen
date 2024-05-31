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

CRITERIA_SUBJECTS = {
    "FIELDS_OF_STUDY": FIELDS_OF_STUDY,
    "UNIVERSITIES": UNIVERSITIES,
    "PROGRAM_TYPES": PROGRAM_TYPES,
    "OPTIONS": OPTIONS,
}  # indicating the part of the subject a criteria

# There are two main group of numbers that we are to figure out:
#  (1) Criteria weight
#  (2) Criteria value for each of its subject values (i.e. each university if the subject is 'U)
class Criteria:
    def __init__(
        self, name: str, subject: str, weight:float, default_value:float, is_constant_value:bool
    ) -> None:
        assert subject in CRITERIA_SUBJECTS

        self.name = name
        self.subject = subject
        self.weight = weight
        self.is_constant_value = is_constant_value
        self.values = {
            s: default_value for s in CRITERIA_SUBJECTS[subject]
        }  # all valued from 0.0 to 1.0

    def get_score(self, option: tuple, weighted=True) -> float:
        score = 0.0
        if self.subject == "FIELDS_OF_STUDY":
            score = self[option[0]]
        elif self.subject == "UNIVERSITIES":
            score = self[option[1]]
        elif self.subject == "PROGRAM_TYPES":
            score = self[option[2]]
        elif self.subject == "OPTIONS":
            score = self[option]

        if weighted:
            return self.weight * score
        else:
            return score

    def __getitem__(self, key: str) -> float:
        return self.values[key]

    def __setitem__(self, key: str, val: float) -> None:
        if val < 0.0 or val > 1.0:
            raise ValueError("Value should be in range of 0.0 t0 1.0")
        self.values[key] = val

