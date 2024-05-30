# This code is only for algorithmic porpuses and it's by no means optimized!

import json
from data_structures import OPTIONS, Criteria, ListCheen

CRITERION_PATH = "./initial_data/criterion.json"
CONSTANT_VALUES_PATH = "./initial_data/constant_values/"


class ListCheen:
    def __init__(self) -> None:
        # initiate the criterion
        self.criterion = {}
        with open(CRITERION_PATH, encoding="utf-8") as f:
            for c_dict in json.load(f):

                self.criterion[c_dict["name"]] = Criteria(
                    c_dict["name"],
                    c_dict["subject"],
                    c_dict["initial_weight"],
                    c_dict["default_value"],
                    c_dict["is_constant_value"],
                )

        # initiate constant values
        for cr in self.criterion.values():
            if cr.is_constant_value:
                with open(
                    CONSTANT_VALUES_PATH + cr.name + ".json", encoding="utf-8"
                ) as f:
                    for key, val in json.load(f).items():
                        # convert "روانشناسی|تهران|روزانه" to tuple
                        key = tuple(key.split("|")) if "|" in key else key

                        cr[key] = val

    def score(self, option) -> float:
        return sum(cr.get_score(option) for cr in self.criterion.values())

    def print_option(self, option) -> None:
        print("option:", option)
        for cr in self.criterion.values():
            print(
                cr.name,
                ": ",
                cr.weight,
                "*",
                cr.get_score(option, weighted=False),
            )
        print("sum:\t", sum(cr.get_score(option) for cr in self.criterion.values()))

    def export_list(self, path="./list.tsv"):
        option2score = {o: self.score(o) for o in OPTIONS}
        with open(path, "w", encoding="utf-8") as outf:
            for line in sorted(
                option2score.items(), key=lambda o2s: o2s[1], reverse=True
            ):
                outf.write(str(line[1]) + "\t" + " ".join(line[0]) + "\n")
        print("list exported to " + path)
