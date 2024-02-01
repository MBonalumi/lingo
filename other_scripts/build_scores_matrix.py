import pandas as pd
import numpy as np
import sys

args = sys.argv[1:]
print(args)
LEN = args[0]
assert LEN in ['4', '5', '6', '7', '8', '9', '10', '11']
LEN = int(LEN)

words = pd.read_csv(f'vocabolari/words{LEN}.csv', header=None, names=['word'])
# words.head()


#build dictionary of scores.
#Translate between lists of [0,1,2] of length LEN and integers from 0 to 2^LEN -1
import itertools
combinations = list(itertools.product([0, 1, 2], repeat=LEN))
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
    scores[i,i] = score(words.word[i], words.word[i])
    for j in range(i+1, len(words)):
        scores[i,j] = score(words.word[i], words.word[j])
        scores[j,i] = score(words.word[j], words.word[i])


#save the matrix
np.save(f'var/scores{LEN}.npy', scores)