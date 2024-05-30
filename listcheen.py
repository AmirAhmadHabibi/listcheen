# This code is only for algorithmic porpuses and it's by no means optimized!

import json
from data_structures import Criteria, ListCheen

CRITERION_PATH = "./initial_data/criterion.json"
CONSTANT_VALUES_PATH = "./initial_data/constant_values/"
USER_INPUT_PATH = "./user_input/"


def initiate_criterion(lc):
    with open(CRITERION_PATH, encoding="utf-8") as f:
        for c_dict in json.load(f):

            lc.criterion[c_dict["name"]] = Criteria(
                c_dict["name"],
                c_dict["subject"],
                c_dict["initial_weight"],
                c_dict["default_value"],
                c_dict["is_constant_value"],
            )


def initiate_constant_values(lc):
    for cr in lc.criterion.values():
        if cr.is_constant_value:
            with open(CONSTANT_VALUES_PATH + cr.name + ".json", encoding="utf-8") as f:
                for key, val in json.load(f).items():
                    # convert "روانشناسی|تهران|روزانه" to tuple
                    key = tuple(key.split("|")) if "|" in key else key

                    cr[key] = val


def ask_user(lc):
    for cr in lc.criterion.values():
        if not cr.is_constant_value:
            with open(USER_INPUT_PATH + cr.name + ".json", encoding="utf-8") as f:
                for key, val in json.load(f).items():
                    # convert "روانشناسی|تهران|روزانه" to tuple
                    key = tuple(key.split("|")) if "|" in key else key
                    cr[key] = val


lc = ListCheen()
initiate_criterion(lc)
initiate_constant_values(lc)
ask_user(lc)
lc.export_list()
lc.print_option(("روانشناسی", "تهران", "روزانه"))
# lc.print_option(("روانشناسی", "تهران", "شبانه"))

# step 0.5: add criteria category and their super weight
# each category should be normalized so that number of criterion wouldn't affect a category's total weight
# TODO

# Step 2: fill in the weights:
# TODO


# Step 3: tune stuff
# TODO

# Step4 : add criteria
# TODO

