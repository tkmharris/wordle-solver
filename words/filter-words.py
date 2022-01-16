wi_file = 'words.txt'
wo_file = '5letterwords.txt'

# filter function
def wordle_word_filter(word):
	if len(word) != 5:
		return False
	if not (word.isalpha() and word.islower()):
		return False
	return True

if __name__=="__main__":

	# load words, strip newlines
	with open(wi_file, 'r') as f:
		words = f.readlines()
	words = [word.strip() for word in words]

	# retain 5-alphabet-letter, lower-case words only
	words = filter(wordle_word_filter, words)

	# words to upper-case, restore newlines and write to file
	words = [word.upper() +'\n' for word in words]
	with open(wo_file, 'w') as f:
		f.truncate(0)
		f.writelines(words)