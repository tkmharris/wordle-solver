"""
Helper functions for Wordle solver.
"""

import json

class NoWordError(Exception):
    """
    Error to record empty list of words.
    """

class FailedToSolveError(Exception):
    """
    Error to record failure to solve puzzle.
    """

def load_words(words_json):
    """
    Get list of words from json file of type {str:bool};
    include word if boolean value is True.

    words_json: json file; words encode
    rtype: [str]
    """
    with open(words_json, encoding='UTF-8') as json_file:
        word_dict = json.load(json_file)
    words = [
        word
        for word in word_dict.keys() if word_dict[word]
    ]
    return words


def character_counts(words):
    """
    Count total occurences of characters in list of words.

    words: [str]
    rtype: {str:int} (len(str) == 1)
    """
    probs = {char: 0 for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    for word in words:
        for char in word:
            probs[char] += 1
    return probs

def position_character_counts(words, positions):
    """
    Count total occurences of characters in each position in a list of words.

    words: [str]
    rtype: {int:{str:int}} (len(str) == 1)
    """
    counts = {
        pos: {char: 0 for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
        for pos in positions
    }
    for pos in positions:
        for word in words:
            counts[pos][word[pos]] += 1
    return counts
