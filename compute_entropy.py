import pandas as pd
import numpy as np

def compute_entropy(words, candidate_answers, scores_matrix):
    #check that words and candidate_answers are pd.dataframe column
    assert (isinstance(words, pd.Series) or isinstance(words, pd.DataFrame))\
        and isinstance(candidate_answers, pd.Series), "words and candidate_answers must be pd.Series, e.g. dataset['column']"

    indices = np.sort(words.index)
    indices_ans = np.sort(candidate_answers.index)
    entropies = []

    for i_guess in indices:
        i_scores = []
        for i_ans in indices_ans:
            i_scores.append(scores_matrix[i_guess, i_ans])

        # i_scores_counts = pd.DataFrame(i_scores).value_counts()
        # i_scores_idx =  i_scores_counts.index.map(lambda x: x[0]).to_numpy()
        i_scores_amt = pd.DataFrame(i_scores).value_counts().to_numpy()

        i_probs = i_scores_amt / len(indices)
        i_entropy = i_probs * np.log2(1/i_probs)

        entropies.append(np.sum(i_entropy))

    return np.array(entropies)