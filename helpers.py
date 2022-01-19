import json 

def load_words(words_json):
	with open(words_json) as json_file:
		word_dict = json.load(json_file)
	words = [
		word 
		for word in word_dict.keys() if word_dict[word]
	]
	return words

def character_counts(words):
	probs = {char: 0 for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
	for word in words:
		for char in word:
			probs[char] += 1
	return probs

def position_character_counts(words, positions):
	counts = {
		pos: {char: 0 for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
		for pos in positions
	}
	for pos in positions:
		for word in words:
			counts[pos][word[pos]] += 1
	return counts