import sys, random, json
import strategies
from helpers import load_words

class NoWordError(Exception):
	pass

class Wordle:

	def __init__(self, 
				 hidden_word, 
				 strategy,
				 words=None, 
				 words_json='words/5letterwords.json'
				 ):

		self.word = hidden_word
		self.strategy = strategy
		
		if not words:
			self.words = load_words(words_json)
		else:
			self.words = words 
		
		self.reset_puzzle()

				
	def reset_puzzle(self):
		self.guesses = []
		self.possible_words = self.words
		self.guesses = []
		self.greens = {}
		self.yellows = {}
		self.blacks = []

	def update_possible_words(self):
			# filter out words prohibited by known constraints
			# or that we have tried
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
			tried_filter = lambda word: not word in self.guesses
			filters = [black_filter, green_filter, yellow_filter, tried_filter]
			
			self.possible_words = [
				word for word in self.possible_words 
				if all([col_filter(word) for col_filter in filters])
			]

	def guess(self):
		guess = self.strategy(
					possible_words=self.possible_words,
					greens=self.greens,
					yellows=self.yellows,
					blacks=self.blacks
				)
		return guess

	def play_turn(self, verbose=False):

		try:
			guess = self.guess()
		except NoWordError:
			sys.exit("Solve failed")

		# add guess to guesses
		self.guesses.append(guess)

		# log guess
		if verbose:
			print(f"Guess: {guess}")

		# update game state
		for pos, char in enumerate(guess):
			# add green flag for correctly guessed letters in the right position
			# remove yellow flags for that position
			if char == self.word[pos]:
				self.greens[char] = pos
				for char, positions in self.yellows.items():
					try:
						positions.remove(pos)
					except ValueError:
						pass
			# add yellow flag for correctly guessed characters in wrong position
			# include note of wrong position
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


	def play(self, max_guesses=100, verbose=False):

		tries = 0
		while tries < max_guesses:
			tries += 1
			solved, guesses = self.play_turn(verbose=verbose)
			if solved:
				
				# reset game
				self.reset_puzzle()

				# log success
				if verbose:
					print(f"Solved in {guesses} guesses")

				return guesses
		print(f"Out of tries ({max_guesses})")

			


	

"""
# test
puzzle = Wordle("ZEBRA", strategy=strategies.naive_guess)
puzzle.play(verbose=True)
"""