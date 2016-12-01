# 6.00 Problem Set 3A Solutions
#
# The 6.00 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
#

import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
TOTAL_SCORE = 0
G_HAND = {}

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print "  ", len(wordlist), "words loaded."
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

	The score for a word is the sum of the points for letters
	in the word multiplied by the length of the word, plus 50
	points if all n letters are used on the first go.

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    returns: int >= 0
    """
    # TO DO...
    score = 0
    for letter in word:
        if letter in SCRABBLE_LETTER_VALUES:
            score += SCRABBLE_LETTER_VALUES[letter]
        else:
            return "was not a word"
    if len(word) == n:
        return (score * len(word)) + 50
    else:
        return score * len(word)

#print get_word_score("bodacious", 9)

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print letter,              # print all on the same line
    print                               # print an empty line

#
# Make sure you understand how this function works and what it does!
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = n / 3

    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1

    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
	In other words, this assumes that however many times
	a letter appears in 'word', 'hand' has at least as
	many of that letter in it.

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """
    # TO DO ...
    new_hand = dict(hand)
    for letter in word:
        if letter in new_hand.keys() and new_hand[letter] > 0:
            new_hand[letter] = new_hand[letter] - 1
            if new_hand[letter] == 0:
                del new_hand[letter]

    return new_hand

#hand = deal_hand(7)
# hand = {'a':1, 'q':1, 'l':2, 'm':1, 'u':1, 'i':1}
# display_hand(hand)
# hand = update_hand(hand, 'quail')
# print hand
# display_hand(hand)

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """
    # TO DO...
    valid = True
    count = 0
    if word in word_list:
        for letter in hand.keys():
            if word.count(letter) > 0:
                count += 1
                if hand[letter] < word.count(letter):
                    return False
        if count == 0:
            return False
    else:
        return False
    return True



def calculate_handlen(hand):
    handlen = 0
    for v in hand.values():
        handlen += v
    return handlen

#
# Problem #4: Playing a hand
#
def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.

    * The user may input a word.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * When a valid word is entered, it uses up letters from the hand.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing a single
      period (the string '.') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings

    """
    # TO DO ...
    #print hand
    if not hand:
        print("Total score: {}".format(TOTAL_SCORE))
    else:
        global TOTAL_SCORE
        score = 0
        print("Current Hand: ")
        display_hand(hand)
        word = raw_input("Enter word, or a \".\" to indicate that you are finished: ")

        if word == ".":
            print("Total score: {}".format(TOTAL_SCORE))
        else:
            valid = is_valid_word(word, hand, word_list)
            if valid == True:
                new_hand = update_hand(hand,word)
                score = get_word_score(word, HAND_SIZE)
                TOTAL_SCORE = TOTAL_SCORE + score
                print("\"{}\" earned {} points. Total: {} points".format(word, score, TOTAL_SCORE))
                play_hand(new_hand, word_list)
            else:
                print "Invalid word, please try again"
                play_hand(hand, word_list)

    #
# Problem #5: Playing a game
# Make sure you understand how this code works!
#
def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.

    * Asks the user to input 'n' or 'r' or 'e'.

    * If the user inputs 'n', let the user play a new (random) hand.
      When done playing the hand, ask the 'n' or 'e' question again.

    * If the user inputs 'r', let the user play the last hand again.

    * If the user inputs 'e', exit the game.

    * If the user inputs anything else, ask them again.
    """
    # TO DO...
    choice = raw_input("Plese input a choice (n - new game, r - replay last game, e - exit the game): ")
    global G_HAND
    global TOTAL_SCORE
    TOTAL_SCORE = 0

    if choice == "n":
        G_HAND = deal_hand(HAND_SIZE)
        play_hand(G_HAND,word_list)
    elif choice == "r":
        if not G_HAND:
            print("no previous hand, new hand created!")
            G_HAND = deal_hand(HAND_SIZE)
            play_hand(G_HAND,word_list)
        else:
            play_hand(G_HAND,word_list)
    elif choice == "e":
        quit()
    else:
        print("plese select a choice again...")

    play_game(word_list)


#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)


#problem 3
# hand = {'a': 3, 'p': 2, 'r': 1, 'u': 2, 't': 1}
# print is_valid_word("honey", hand, word_list)

#problem 4
#play_hand(deal_hand(HAND_SIZE), word_list)
