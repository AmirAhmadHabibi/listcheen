# This code is only for algorithmic porpuses and it's by no means optimized!

import json
from data_structures import OPTIONS, Criterion

criteria_PATH = "./initial_data/criteria.json"
CONSTANT_VALUES_PATH = "./initial_data/constant_values/"
CATEGORY_WEIGHT_PATH = "./initial_data/category_weight.json"


class ListCheen:
    def __init__(self) -> None:

        # all criteria under each subject would be normalized by the number of cri and then multiplied by subject weight
        # so that number of criteria wouldn't affect a category's total weight
        with open(CATEGORY_WEIGHT_PATH, encoding="utf-8") as f:
            self.category_weight = json.load(f)

        # initiate the criteria
        self.criteria = {}
        self.cat_count = {}
        with open(criteria_PATH, encoding="utf-8") as f:
            for c_dict in json.load(f):
                self.criteria[c_dict["name"]] = Criterion(
                    c_dict["name"],
                    c_dict["category2weight"],
                    c_dict["default_value"],
                    c_dict["different_for_each_option"],
                    c_dict["is_constant_value"],
                )

                for cat in c_dict["category2weight"].keys():
                    if cat in self.cat_count:
                        self.cat_count[cat] += 1.0
                    else:
                        self.cat_count[cat] = 1.0

        # initiate constant values
        for cr in self.criteria.values():
            if cr.is_constant_value:
                with open(
                    CONSTANT_VALUES_PATH + cr.name + ".json", encoding="utf-8"
                ) as f:
                    for key, val in json.load(f).items():
                        # convert "روانشناسی|تهران|روزانه" to tuple
                        key = tuple(key.split("|")) if "|" in key else key

                        cr[key] = val

    def get_option_vector(self, option) -> dict:
        """
        used when comparing two options and tuning their weights
        """
        op_dict = {}

        for cr in self.criteria.values():
            for c, w in cr.category2weight.items():
                name = c[0] + "|" + cr.name
                weight = w
                val = cr.get_score(option, weighted=False, cat=c)
                normalization_factor = self.category_weight[c] / self.cat_count[c]
                op_dict[name] = [weight, val, normalization_factor]
        return op_dict

    def score(self, option) -> float:
        score_sum = 0.0
        for cr in self.criteria.values():
            for c, w in cr.category2weight.items():
                score_sum += (
                    cr.get_score(option, cat=c)
                    * self.category_weight[c]
                    / self.cat_count[c]
                )
        return score_sum

    def print_option(self, option) -> None:
        print("option:", option)
        for cr in self.criteria.values():
            for c, w in cr.category2weight.items():
                print(
                    cr.name,
                    ": ",
                    self.category_weight[c],
                    "*",
                    w,
                    "*",
                    cr.get_score(option, weighted=False, cat=c),
                    "/",
                    self.cat_count[c],
                )
        print("sum:\t", self.score(option))

    def export_list(self, path="./list.tsv"):
        option2score = {o: self.score(o) for o in OPTIONS}
        with open(path, "w", encoding="utf-8") as outf:
            for line in sorted(
                option2score.items(), key=lambda o2s: o2s[1], reverse=True
            ):
                outf.write(str(round(line[1], 4)) + "\t" + " ".join(line[0]) + "\n")
        print("list exported to " + path)
