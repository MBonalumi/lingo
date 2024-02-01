import re
import numpy as np

class filter_word:
    def __init__(self, length:int) -> None:
        self.length = length
        self.filter_is = ['.' for _ in range(length)]
        self.filter_isnot = ['' for _ in range(length)]
        self.filters_contain = []

    def apply(self, dataset):
        #build regex out of filters specifications
        # filter_is_isnot = [self.filter_is[i] if self.filter_is[i] != '.' else f'[^{self.filter_isnot[i]}]' for i in range(len(self.filter_is))]
        filter_is_isnot = self.filter_is.copy()
        for i in range(len(self.filter_is)):
            if self.filter_is[i] == '.' and self.filter_isnot[i] != '':
                filter_is_isnot[i] = f'[^{self.filter_isnot[i]}]'
        re_is_isnot = re.compile('^' + ''.join(filter_is_isnot) + '$')
        re_contain = [re.compile('^' + ''.join(contain) + '$') for contain in self.filters_contain]

        #apply filters
        filtered_mask = dataset.str.match(re_is_isnot)
        for r in re_contain:
            filtered_mask = filtered_mask & dataset.str.match(r)
        return dataset[filtered_mask]

    def letter_is(self, position:int, letter:str) -> None:
        assert len(letter) == 1, "letter must be a single character"
        self.filter_is[position] = letter.upper()

    def letter_isnot(self, position:int, letters:str) -> None:
        self.filter_isnot[position] = self.filter_isnot[position] + letters.upper()

    def word_contains(self, letter:str, quantity=1) -> None:
        assert quantity > 0 and quantity <= self.length, "quantity must be between 1 and word length"
        assert len(letter) == 1, "letter must be a single character"
        letter = letter.upper()
        self.filters_contain.append(    f".*" + ''.join([letter + f".*" for _ in range(quantity)])   )

    def word_contains_exactly(self, letter:str, quantity=1) -> None:
        assert quantity > 0 and quantity <= self.length, "quantity must be between 1 and word length"
        assert len(letter) == 1, "letter must be a single character"
        letter = letter.upper()
        self.filters_contain.append(    f"[^{letter}]*" + ''.join([letter + f"[^{letter}]*" for _ in range(quantity)])   )

    # def word_contains_not(self, letter:str, quantity=2) -> None:
    #     assert quantity > 1 and quantity <= self.length,\
    #         "quantity must be between 2 and word length, since we are saying that there is one X but not 2 Xs"
    #     assert len(letter) == 1, "letter must be a single character"


    def filter(self, guess:str, feedback:list|np.ndarray) -> None:
        guess = guess.upper()
        letters_to_exclude = []
        letters_contained = []
        letters_contained_amt = []
        for i,f in enumerate(feedback):
            if f == 2:
                self.letter_is(i, guess[i])
            elif f == 1:
                #count the number of times the letter is contained
                if guess[i] not in letters_contained:
                    letters_contained.append(guess[i])
                    letters_contained_amt.append(1)
                else:
                    letters_contained_amt[letters_contained.index(guess[i])] += 1
                self.letter_isnot(i, guess[i])
            elif f == 0:
                #add only once, to avoid duplicates that can mess up.
                #   e.g. if the guess is "AMACA" and we find out that our word has exactly 1 a,
                #       we have to indefinetly remove As to ensure to not have it in "string_exclude" 
                if guess[i] not in letters_to_exclude:
                    letters_to_exclude.append(guess[i])
        
        for i, l_c in enumerate(letters_contained):
            #if the word is also in "exclude", then we know the exact amount of time it appears,
            #   add with word_contains_exactly instead of word_contains
            if l_c in letters_to_exclude:
                self.word_contains_exactly(l_c, letters_contained_amt[i])
                # remove from letters_to_exclude
                letters_to_exclude.remove(l_c)
            else:
                self.word_contains(l_c, letters_contained_amt[i])
        
        string_exclude = ''.join(letters_to_exclude)
        for l_e in np.arange(len(guess))[np.array(feedback) != 2]:
            self.letter_isnot(l_e, string_exclude)