import itertools

#TODO: only valid for 6 letters
combinations = list(itertools.product([0, 1, 2], repeat=6))
conversion_dict_l2i = {combination: index for index, combination in enumerate(combinations)}
conversion_dict_i2l = {index: combination for index, combination in enumerate(combinations)}

#TODO: only valid for 6 letters
best_initial_guesses = {
    'A': 'INTERO',  'B': 'CANORI',  'C': 'NOTARE',  'D': 'TIRANO',  'E': 'ORLATI',  'F': 'ORLATI',  'G': 'TEORIA',
    'I': 'ONESTA',  'L': 'ROTAIE',  'M': 'ROTAIE',  'N': 'COVATI',  'O': 'SENATI',  'P': 'ROTAIE',  'Q': 'STORIE',
    'R': 'TENACI',  'S': 'PERITA',  'T': 'PERCIO',  'U': 'INTESA',  'V': 'GIRATO',  'Z': 'GUARDI'
}