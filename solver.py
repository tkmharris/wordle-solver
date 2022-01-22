"""
Wordle solver class.
"""

import sys
from helpers import load_words, NoWordError, FailedToSolveError

class Wordle:

    def __init__(self,
        hidden_word,
        strategy,
        words=None,
        words_json='words/5letterwords.json'
        ):
        """
        Initialize puzzle.

        hidden_word: str
        strategy: method from strategies.py
        words: [str]
        words_json: json file
        rtype: None
        """

        self.word = hidden_word
        self.strategy = strategy

        # if a list of valid words is not supplied, load them from file.
        if not words:
            self.words = load_words(words_json)
        else:
            self.words = words

        # set initial state
        self.reset_puzzle()


    def reset_puzzle(self):
        """
        Set puzzle to initial state:
        no guesses made, no info known, no words excluded from base list.

        rtype: None
        """
        self.guesses = []
        self.possible_words = self.words
        self.guesses = []
        self.greens = {}
        self.yellows = {}
        self.blacks = []


    def update_possible_words(self):
        """
        Update the list of possible guesses given known letter placement info.

        rtype: None
        """

        # filters to rule out words with letters in certain positions
        black_filter = lambda word: not any([
                black in word
                for black in self.blacks
            ])
        green_filter = lambda word: all([
                word[pos] == char
                for char, pos in self.greens.items()
            ])
        yellow_filter = lambda word: all([
                char in word and all([
                        word[pos] != char for pos in positions
                    ])
                for char, positions in self.yellows.items()
            ])
        # filter to rule out past guesses
        tried_filter = lambda word: not word in self.guesses

        # apply all filters to self.possible_words
        filters = [black_filter, green_filter, yellow_filter, tried_filter]
        self.possible_words = [
            word for word in self.possible_words
            if all([col_filter(word) for col_filter in filters])
        ]


    def guess(self):
        """
        Pick a valid guess given current puzzle state.

        rtype: str
        """
        guess = self.strategy(
                    possible_words=self.possible_words,
                    greens=self.greens,
                    yellows=self.yellows,
                    blacks=self.blacks
                )
        return guess


    def play_turn(self,
            verbose=False):
        """
        Make a single guess and update puzzle state accordingly.
        Return boolean recording if guess is correct and int of guesses so far.
        If there are no valid guesses, exit.

        verbose: bool
        rtype: (bool, int)
        """
        try:
            guess = self.guess()
        except NoWordError:
            sys.exit("Solve failed")

        # add guess to guesses; print to terminal if verbose
        self.guesses.append(guess)
        if verbose:
            print(f"Guess: {guess}")

        # update green, yellow, black letters info
        for pos, char in enumerate(guess):

            if char == self.word[pos]:
                # add green flag for correctly guessed letters in the right position
                self.greens[char] = pos
                # remove yellow flags for that position
                for _, positions in self.yellows.items():
                    try:
                        positions.remove(pos)
                    except ValueError:
                        pass
            # add yellow flag for correctly guessed characters in wrong position
            elif char in self.word:
                if self.yellows.get(char):
                    self.yellows[char].append(pos)
                else:
                    self.yellows[char] = [pos]
            # add black flag for characters not in word
            else:
                self.blacks.append(char)

        # update list of words given green, yellow, black flags
        self.update_possible_words()

        return (guess == self.word), len(self.guesses)


    def play(self,
        max_guesses=100,
        verbose=False):
        """
        Play full game. Return number of guesses until correct solution.
        Raise error if no possible words remain or we exceed max number of guesses.

        max_guesses: int
        verbose: bool
        rtype: int
        """

        tries = 0
        while tries < max_guesses:

            try:
                solved, guesses = self.play_turn(verbose=verbose)
                tries += 1
                if solved:
                    # log success
                    if verbose:
                        print(f"Solved in {guesses} guesses")
                        # reset game
                    self.reset_puzzle()
                    return guesses

            except NoWordError:
                raise FailedToSolveError("Out of possible words.")

        raise FailedToSolveError("Ran out of guesses.")
                    