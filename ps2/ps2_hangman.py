# 6.00 Problem Set 3
#
# Hangman
#


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import random
import string

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
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# actually load the dictionary of words and point to it with
# the wordlist variable so that it can be accessed from anywhere
# in the program
wordlist = load_words()

# your code begins here!
def hide_word(word):
    new_word = []
    for w in word:
        new_word.append("_")
    return new_word

def place_letter(hidden_word, choice, word):
    word_state = ""
    count = 0
    for letter in word:
        if choice == letter:
            hidden_word[count] = str(choice)
        count = count + 1

    for w in hidden_word:
        word_state = word_state + w

    return word_state

def check_letter(guesses, word, hidden_word, letters):
    print "-----------"
    print "You have " + str(guesses) + " gusses left"
    print "Available letters: " + str(letters)
    choice = raw_input("Please guess a letter: ")
    if choice not in letters:
        print "Incorrect selection, try again!"
        check_letter(guesses, word, hidden_word, letters)
    letters = letters.replace(choice, "")
    if choice in word:
        print "Good guess: " + place_letter(hidden_word, choice, word)
        #recursively call function
        if ''.join(hidden_word) == word:
            print "-----------"
            print "Congratulations, you won!"
        else:
            check_letter(guesses, word, hidden_word, letters)
    else:
        guesses = guesses - 1
        if guesses < 1:
            print "-----------"
            print "Oops, look like there are no more guesses left, try again!"
        else:
            #recursively call function
            print "Oops! That letter is not in my word: " + place_letter(hidden_word, choice, word)
            check_letter(guesses, word, hidden_word, letters)

guesses = 8
letters = "abcdefghijklmnopqrstuvwxyz"
word = choose_word(load_words())
hidden_word = hide_word(word)
print word
print "Welcome to the game, Hangman!"
print "I am thinking of a word that is 4 letters long."
check_letter(guesses, word, hidden_word, letters)
