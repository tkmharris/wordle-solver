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
total_guesses = 0
for sol in sols:
	success, guesses = test_solver(sol, strategy=strategies.more_informed_guess, words_json=words_json)
	if success:
		solved += 1
		total_guesses += guesses 
print(f"number solved: {solved}/{len(sols)} ({100*solved/len(sols)}%)")
print(f"average guesses per solve: {round(total_guesses/solved, 3)}")
toc = time.perf_counter()
print(f"time to solve {len(sols)} puzzles: {round(toc-tic, 3)}s")
