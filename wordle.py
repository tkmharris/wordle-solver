import sys, random

class NoWordError(Exception):
	pass

class Wordle:

	def __init__(self, hidden_word):
		self.word = hidden_word
		self.guesses = 0
		self.greens = []
		self.yellows = []
		self.blacks = []


	def play_turn(self, player):

		self.guesses += 1

		try:
			guess = player.guess(
					greens=self.greens,
					yellows=self.yellows,
					blacks=self.blacks
				)
		except NoWordError:
			sys.exit("Solve failed")

		print(f"Guess: {guess}")

		for pos, char in enumerate(guess):
			if char == self.word[pos]:
				self.greens.append((pos, char))
			elif char in self.word:
				self.yellows.append((pos, char))
			else:
				self.blacks.append(char)

		return (guess == self.word), self.guesses

	def play(self, player):

		while True:
			solved, guesses = self.play_turn(player)
			if solved:
				print(f"Solved in {guesses} guesses")
				break

			
class Player:

	def __init__(self, words=None, words_path='words/5letterwords.txt'):
		
		if not words:
			with open(words_path, 'r') as f:
				self.words = [
					word.strip() for word in f.readlines()
				]
		else:
			self.words = words 

	def select_word(self, possible_words):
		"""
		Mechanism to select the best guess from a list of valid guesses.
		Not yet properly implemented; for now pick one at random.
		"""
		return random.choice(possible_words)

	def guess(self, greens, yellows, blacks):

		# filter out words prohibited by known constraints
		black_filter = lambda word: not any([
				black in word
				for black in blacks
			])
		green_filter = lambda word: all([
				word[green[0]] == green[1]
				for green in greens
			])

		yellow_filter = lambda word: all([
				yellow[1] in word and word[yellow[0]] != yellow[0]
				for yellow in yellows
			])
		filters = [black_filter, green_filter, yellow_filter]
		possible_words = [
			word for word in self.words 
			if all([col_filter(word) for col_filter in filters])
		]

		if possible_words == []:
			raise NoWordError

		guess = self.select_word(possible_words)

		return guess

"""
# test
player = Player()
puzzle = Wordle("SOLAR")
puzzle.play(player)
"""