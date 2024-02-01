import numpy as np
from tqdm import tqdm

import itertools
combinations = list(itertools.product([0, 1, 2], repeat=6))
conversion_dict = {combination: index for index, combination in enumerate(combinations)}
import time

start = time.time()
print("reading list of values")
scores_list = np.load('var/scores6.npy', allow_pickle=True)
end = time.time()
print(f"read in {end-start} seconds")

scores_int = np.zeros((len(scores_list), len(scores_list)), dtype=np.int16)-1

for i in tqdm(range(len(scores_list))):
    for j in range(len(scores_list)):
        scores_int[i,j] = conversion_dict[tuple(scores_list[i,j])]

np.save('var/scores6_int.npy', scores_int)

'''
EXAMPLES (score, word1, word2)

(728, 'ABBAIA', 'ABBAIA')
(726, 'ABBAIA', 'ABBAIO')
(707, 'ABBAIA', 'ABBINA')
(728, 'ABBAIO', 'ABBAIO')
(728, 'AGGIRO', 'AGGIRO')
(10, 'STORMI', 'DICARE')

'''