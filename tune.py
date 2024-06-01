def tune(lc, option1, option2):
    """
    change the weights and values so that option 1 would become greater than option 2
    """
    # 2.1 a - 235.3 b + 243.3 c + 23.1 d > 0
    # a= 0.5, b= 0.4 , c=0.1, d= 1.0
    # change a,b,c,d with minimal sum of abs(delta x) x in a,b,c,d

    # alg:
    # find the direction of change for each weight
    # change each an epsilon and see wich ones are more important
    # should not change the order of the weights as far as possible
    # repeat until the condition is reached
    # if changed order, then give warning

    EPSILON = 0.001
    # option1 = {criterion.name : [weight , normalized_value]}
    print(lc.get_option_vector(option1))
    print(lc.get_option_vector(option2))
    # what if he wants to change values?

    while option1 < option2:
        change = option1 - option2
        # try to make change > 0
        # for each value and weight, change an epsilon in the right direction if doesn't change order
        for cr_name, cr_vals in change.items():
            weight, value, normalization_factor = cr_vals
            if weight * value * normalization_factor < 0:
                direction = -1.0
            else:
                direction = 1.0
            new_weight = weight + direction * EPSILON
            # TODO instead of keep_order, precompute bounds of the number
            if keep_order(cr_name, "weight", new_weight):
                change_weight(cr_name, new_weight)
            if option1 > option2:
                break
            new_value = value + direction * EPSILON
            if keep_order(cr_name, "value", new_value):
                change_value(cr_name, new_value)

    # TODO
