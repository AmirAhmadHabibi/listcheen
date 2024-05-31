import json
from listcheen import ListCheen

USER_INPUT_PATH = "./user_input/"


def ask_user(lc):
    for cr in lc.criterion.values():
        if not cr.is_constant_value:
            with open(USER_INPUT_PATH + cr.name + ".json", encoding="utf-8") as f:
                for key, val in json.load(f).items():
                    # convert "روانشناسی|تهران|روزانه" to tuple
                    key = tuple(key.split("|")) if "|" in key else key
                    cr[key] = val


lc = ListCheen()
ask_user(lc)

lc.export_list()
lc.print_option(("روانشناسی", "تهران", "روزانه"))
# lc.print_option(("روانشناسی", "تهران", "شبانه"))

# Step 2: fill in the weights:
# TODO

# Step 3: tune stuff
# TODO

# Step4 : add criteria
# TODO
