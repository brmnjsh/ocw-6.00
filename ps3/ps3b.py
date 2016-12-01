from ps3a import *
import time
from perm import *


#
#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    # TO DO...
    score = 0
    i = 0
    word = ""
    while i < len(hand):
        perms = get_perms(hand, i)
        for p in perms:
            new_score = get_word_score(p, i)
            if (new_score > score):
                if p in word_list:
                    score = new_score
                    word = p
        i += 1

    return word

#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed,
       the remaining letters in the hand are displayed, and the computer
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    # TO DO ...
    if not hand:
        print("Total score: {}".format(TOTAL_SCORE))
    else:
        global TOTAL_SCORE
        score = 0
        print("Current Hand: ")
        display_hand(hand)
        word = comp_choose_word(hand, word_list)

        if word == ".":
            print("Total score: {}".format(TOTAL_SCORE))
        else:
            valid = is_valid_word(word, hand, word_list)
            if valid == True:
                new_hand = update_hand(hand,word)
                score = get_word_score(word, HAND_SIZE)
                TOTAL_SCORE = TOTAL_SCORE + score
                print("\"{}\" earned {} points. Total: {} points".format(word, score, TOTAL_SCORE))
                comp_play_hand(new_hand, word_list)
            else:
                print("Total score: {}".format(TOTAL_SCORE))
#
# Problem #6C: Playing a game
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    # TO DO...

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

h = deal_hand(HAND_SIZE)
#comp_choose_word(h, word_list)
comp_play_hand(h,word_list)
