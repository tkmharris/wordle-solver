import random
from helpers import character_counts, position_character_counts

def random_guess(possible_words, 
				greens=None, 
				yellows=None, 
				blacks=None):
	"""
	Choose a word at random among remaining words that fit known info
	Raise error if there are no words remaining
	"""
	if possible_words == []:
		raise NoWordError
	guess = random.choice(possible_words)
	return guess

# somehow this informed guess is worse than guessing at random
def informed_guess(possible_words, 
				greens=None, 
				yellows=None, 
				blacks=None):
	"""
	Choose a word among remaining words by selecting the word 
	with the most frequently occurring characters among remaining words
	Raise error if there are no words remaining.

	Somehow this performs worse than selecting randomly?
	"""
	if possible_words == []:
		raise NoWordError

	# calculate character frequencies among remaining words
	char_counts = character_counts(possible_words)

	# select word with most frequently occuring characters in unresolved positions
	free_positions = [
			pos for pos in range(5)
			if pos not in greens.values()
		]
	best_word, best_score = None, 0
	for word in possible_words:
		word_score = sum([
				char_counts[word[pos]]
				for pos in free_positions
			])
		if word_score > best_score:
			best_score = word_score
			best_word = word
	
	return best_word

def more_informed_guess(possible_words, 
				greens=None, 
				yellows=None, 
				blacks=None):
	"""
	Choose a word among remaining words by selecting the word 
	with the most frequently occurring characters among remaining words
	Raise error if there are no words remaining.

	Somehow this performs worse than selecting randomly?
	"""
	if possible_words == []:
		raise NoWordError

	free_positions = [
			pos for pos in range(5)
			if pos not in greens.values()
		]
	# calculate character frequencies among remaining words
	pos_char_counts = position_character_counts(possible_words, free_positions)

	best_word, best_score = None, 0
	for word in possible_words:
		word_score = sum([
				pos_char_counts[pos][word[pos]]
				for pos in free_positions
			])
		if word_score > best_score:
			best_score = word_score
			best_word = word
	
	return best_word
