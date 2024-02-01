import itertools
combinations = list(itertools.product([0, 1, 2], repeat=6))
conversion_dict_l2i = {combination: index for index, combination in enumerate(combinations)}
conversion_dict_i2l = {index: combination for index, combination in enumerate(combinations)}