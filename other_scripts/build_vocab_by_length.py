import pandas as pd
import sys

if __name__ == "__main__":
    # write code to get the arguments
    args = sys.argv[1:]
    print(args)

    length = args[0]
    assert length in ['4', '5', '6', '7', '8', '9', '10', '11']
    length = int(length)

    data = pd.read_csv('vocabolari/vocabolario_60k.txt', sep='\n', header=None, names=['words'])

    #put all words in lowercase
    data['words'] = data['words'].str.upper()
    data['len'] = data['words'].apply(lambda x: len(x))

    words = data[data['len']==length]
    words['words'].describe()

    words['words'].to_csv(f'vocabolari/words{length}.csv', index=False, header=False)
