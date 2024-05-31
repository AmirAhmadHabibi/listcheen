import json
from listcheen import ListCheen

USER_INPUT_PATH = "./user_input/"
USER_INPUT_WEIGHTS_PATH = "./user_input/weights.json"


def ask_user(lc):
    # ask the values:
    for cr in lc.criteria.values():
        if not cr.is_constant_value:
            with open(USER_INPUT_PATH + cr.name + ".json", encoding="utf-8") as f:
                for key, val in json.load(f).items():
                    # convert "روانشناسی|تهران|روزانه" to tuple
                    key = tuple(key.split("|")) if "|" in key else key
                    cr[key] = val
    
    lc.print_option(("روانشناسی", "تهران", "روزانه"))
    # ask the weights:
    with open(USER_INPUT_WEIGHTS_PATH, encoding="utf-8") as f:
        for cat, cat_dict in json.load(f).items():
            # set category super weight from user input
            lc.category_weight[cat] = cat_dict['category_weight']

            # set criterion weight
            for criterion, criterion_weight in cat_dict['criteria'].items():
                lc.criteria[criterion].category2weight[cat] = criterion_weight



lc = ListCheen()
lc.print_option(("روانشناسی", "تهران", "روزانه"))
ask_user(lc)

lc.export_list()
lc.print_option(("روانشناسی", "تهران", "روزانه"))
# lc.print_option(("روانشناسی", "تهران", "شبانه"))


# Step : add criterion
# TODO

# Step : tune stuff
# TODO
