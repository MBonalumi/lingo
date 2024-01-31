import pandas as pd
import numpy as np


words = pd.read_csv('vocabolari/words6.csv', header=None, names=['word'])
# words.head()

import itertools
combinations = list(itertools.product([0, 1, 2], repeat=6))
conversion_dict = {combination: index for index, combination in enumerate(combinations)}

def score(guess, true_word, return_list=False):
    assert len(guess) == len(true_word), 'Guess and true word must have the same length'

    score = [0]*len(true_word)
    todo = list(range(len(guess)))

    for i in range(len(guess)):
        if guess[i] == true_word[i]:
            score[i] = 2
            todo.remove(i)

    true_word_remaining = [true_word[i] for i in todo] if todo else []

    for i in todo:
        if guess[i] in true_word_remaining:
            score[i] = 1
            true_word_remaining.remove(guess[i])

    if return_list:
        return score
    
    return conversion_dict[tuple(score)]


# build the matrix of scores for each pair of words
scores = np.zeros((len(words), len(words)), dtype=list)

from tqdm import tqdm

for i in tqdm(range(len(words))):
    scores[i,i] = score(words.word[i], words.word[i], return_list=True)
    for j in range(i+1, len(words)):
        scores[i,j] = score(words.word[i], words.word[j], return_list=True)
        scores[j,i] = score(words.word[j], words.word[i], return_list=True)


#save the matrix
np.save('var/scores6.npy', scores)