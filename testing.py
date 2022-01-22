from solver import Wordle, NoWordError
import strategies
import time

def test_solver(word, strategy, words_json, verbose=False):

	puzzle = Wordle(word, strategy=strategy, words_json=words_json)

	try:
		guesses = puzzle.play(verbose=verbose)
		success = True

	except NoWordError:
		success = False
		guesses = None

	return success, guesses


sols_to_test = "words/solutions/previous-solutions.txt"
words_json="words/5letterwords.json"

# load past solutions, strip newlines
with open(sols_to_test, 'r') as f:
	sols = [word.strip() for word in f.readlines()]


# test solve rate and average guesses to solve; time operation
tic = time.perf_counter()
solved = 0
solved_in_six = 0
total_guesses = 0
for sol in sols:
	puzzle_guesses = 0
	success, guesses = test_solver(sol, strategy=strategies.most_frequent_characters_by_position_guess, words_json=words_json)
	if success:
		solved += 1
		total_guesses += guesses 
		if guesses <= 6:
			solved_in_six += 1
print(f"number solved: {solved}/{len(sols)} ({100*solved/len(sols)}%)")
print(f"number solved in <=6 guesses: {solved_in_six}/{len(sols)} ({round(100*solved_in_six/len(sols), 3)}%)")
print(f"average guesses per solve: {round(total_guesses/solved, 3)}")
toc = time.perf_counter()
print(f"time to solve {len(sols)} puzzles: {round(toc-tic, 3)}s")
