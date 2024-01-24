import pandas as pd
import numpy as np


words6 = pd.read_csv('vocabolari/words6.csv', header=None, names=['word'])
words6.head()


score_to_int = lambda score: sum([score[-1-i]*10**i for i in range(len(score))])
int_to_score = lambda integer: [int(d) for d in str(integer)]

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
    
    return score_to_int(score)


# build the matrix of scores for each pair of words
scores = np.zeros((len(words6), len(words6)), dtype=np.int32)

from tqdm import tqdm

for i in tqdm(range(len(words6))):
    for j in range(i+1, len(words6)):
        scores[i,j] = score(words6.word[i], words6.word[j])
        scores[j,i] = score(words6.word[j], words6.word[i])


#save the matrix
np.save('var/scores6.npy', scores)