# 6.00 Problem Set 4
#
# Caesar Cipher Skeleton
#
import string
import random

WORDLIST_FILENAME = "words.txt"

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
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
    wordlist = line.split()
    print "  ", len(wordlist), "words loaded."
    return wordlist

wordlist = load_words()

def is_word(wordlist, word):
    """
    Determines if word is a valid word.

    wordlist: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordlist.

    Example:
    >>> is_word(wordlist, 'bat') returns
    True
    >>> is_word(wordlist, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in wordlist

def random_word(wordlist):
    """
    Returns a random word.

    wordlist: list of words
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

def random_string(wordlist, n):
    """
    Returns a string containing n random words from wordlist

    wordlist: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordlist: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words


    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    """
    Returns a fable in encrypted text.
    """
    f = open("fable.txt", "r")
    fable = str(f.read())
    f.close()
    return fable


# (end of helper code)
# -----------------------------------

#
# Problem 1: Encryption
#
def build_coder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: -27 < int < 27
    returns: dict

    Example:
    >>> build_coder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)
    """
    ### TODO.
    alphabet = (' ','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
    cipher = {}
    count = 0
    shifted = shift
    for c in alphabet:
        if count >= 0 and count <= 26:
            if alphabet[count] not in cipher.keys():
                cipher[alphabet[count]] = alphabet[shifted]

            if count == 26 - shift:
                shifted = 0
            else:
                shifted += 1
        elif count >= 27 and count <= 53:
            if count == 27:
                shifted = count + shift

            if alphabet[count] not in cipher.keys():
                cipher[alphabet[count]] = alphabet[shifted]

            if count == 53 - shift:
                shifted = 27
            else:
                shifted += 1

        count += 1
    return cipher

#build_coder(3)

def build_encoder(shift):
    """
    Returns a dict that can be used to encode a plain text. For example, you
    could encrypt the plain text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)

    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_encoder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    ### TODO.
    return build_coder(shift)

#build_encoder(3)

def build_decoder(shift):
    """
    Returns a dict that can be used to decode an encrypted text. For example, you
    could decrypt an encrypted text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    >>>decrypted_text = apply_coder(plain_text, decoder)

    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_decoder(3)
    {' ': 'x', 'A': 'Y', 'C': ' ', 'B': 'Z', 'E': 'B', 'D': 'A', 'G': 'D',
    'F': 'C', 'I': 'F', 'H': 'E', 'K': 'H', 'J': 'G', 'M': 'J', 'L': 'I',
    'O': 'L', 'N': 'K', 'Q': 'N', 'P': 'M', 'S': 'P', 'R': 'O', 'U': 'R',
    'T': 'Q', 'W': 'T', 'V': 'S', 'Y': 'V', 'X': 'U', 'Z': 'W', 'a': 'y',
    'c': ' ', 'b': 'z', 'e': 'b', 'd': 'a', 'g': 'd', 'f': 'c', 'i': 'f',
    'h': 'e', 'k': 'h', 'j': 'g', 'm': 'j', 'l': 'i', 'o': 'l', 'n': 'k',
    'q': 'n', 'p': 'm', 's': 'p', 'r': 'o', 'u': 'r', 't': 'q', 'w': 't',
    'v': 's', 'y': 'v', 'x': 'u', 'z': 'w'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    ### TODO.
    alphabet = (' ','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
    cipher = {}
    count = 0
    shifted = shift
    for c in alphabet:
        if count >= 0 and count <= 26:
            if alphabet[shifted] not in cipher.keys():
                cipher[alphabet[shifted]] = alphabet[count]

            if count == 26 - shift:
                shifted = 0
            else:
                shifted += 1
        elif count >= 27 and count <= 53:
            if count == 27:
                shifted = count + shift

            if alphabet[shifted] not in cipher.keys():
                cipher[alphabet[shifted]] = alphabet[count]

            if count == 53 - shift:
                shifted = 27
            else:
                shifted += 1

        count += 1
    return cipher

#build_decoder(3)

def apply_coder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text

    Example:
    >>> apply_coder("Hello, world!", build_encoder(3))
    'Khoor,czruog!'
    >>> apply_coder("Khoor,czruog!", build_decoder(3))
    'Hello, world!'
    """
    ### TODO.
    word = ''
    for c in text:
        if c in coder.keys():
            word += coder[c]
        else:
            word += c
    return word

#apply_coder("Hello, world!", build_encoder(3))
#apply_coder("Khoor,czruog!", build_decoder(3))

def apply_shift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. The empty space counts as the 27th letter of the alphabet,
    so spaces should be replaced by a lowercase letter as appropriate.
    Otherwise, lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.

    text: string to apply the shift to
    shift: amount to shift the text
    returns: text after being shifted by specified amount.

    Example:
    >>> apply_shift('This is a test.', 8)
    'Apq hq hiham a.'
    """
    ### TODO.
    return apply_coder(text, build_encoder(shift))

# print apply_shift('Apq hq hiham a.', -8)

#
# Problem 2: Codebreaking.
#
def find_best_shift(wordlist, text):
    """
    Decrypts the encoded text and returns the plaintext.

    text: string
    returns: 0 <= int 27

    Example:
    >>> s = apply_coder('Hello, world!', build_encoder(8))
    >>> s
    'Pmttw,hdwztl!'
    >>> find_best_shift(wordlist, s) returns
    8
    >>> apply_coder(s, build_decoder(8)) returns
    'Hello, world!'
    """
    ### TODO
    i = 0
    new_text = ''
    while True:
        t = apply_coder(text, build_decoder(i))

        if is_word(wordlist, t): #check if all of the text is a single work
            return t
        else:
            j = 0
            decrypt = ''
            while True:
                if is_word(wordlist,t[:j]):
                    k = j + 1
                    if t[j:k] is not ' ' and len(t[j:k]) != 0:
                        j += 1
                    elif t[j:k] is ' ':
                        decrypt = t.split()
                        for w in decrypt:
                            if not is_word(wordlist,w):
                                return 'failed to decrypt'

                        return i

                else:
                    if j == len(text):
                        break
                    j += 1
            i += 1
        if i == 27:
            return "failed to decrypt"

# s = apply_coder('Hello, world!', build_encoder(17))
# shift = find_best_shift(wordlist, s)
# print shift
# s = apply_coder(s, build_decoder(shift))
# print s


#
# Problem 3: Multi-level encryption.
#
def apply_shifts(text, shifts):
    """
    Applies a sequence of shifts to an input text.

    text: A string to apply the Ceasar shifts to
    shifts: A list of tuples containing the location each shift should
    begin and the shift offset. Each tuple is of the form (location,
    shift) The shifts are layered: each one is applied from its
    starting position all the way through the end of the string.
    returns: text after applying the shifts to the appropriate
    positions

    Example:
    >>> apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    """
    ### TODO.
    t = text
    for shift in shifts:
        if t == text:
            t = apply_coder(t[shift[0]:], build_encoder(shift[1]))
        else:
            t = t[:shift[0]] + apply_coder(t[shift[0]:], build_encoder(shift[1]))
    return t

# e = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
# print e

#
# Problem 4: Multi-level decryption.
#
def find_best_shifts(wordlist, text):
	return find_best_shifts_rec(wordlist, text, len(text))

def find_best_shifts_rec(wordlist, text, start):
	final = ''
	fail = False
	t = text[len(text) - start:]
	if is_word(wordlist, t):
		return t
	else:
		i = 0
		found = False
		while i <= 26:
			n_text = apply_coder(t, build_encoder(i))
			words = n_text.split()

			if is_word(wordlist, words[0]):
				start = len(n_text) - len(words[0]) - 1

				if start <= 1:
					print start
					print 'reached the end'
					return words[0]

				n = find_best_shifts_rec(wordlist, n_text, start)

				if n is not False:
					found = True
					return words[0] + ' ' + n

			if i is 26 and found is False:
				return False

			i += 1
	# j = 1
	# while j <= 26:
	# 	t = apply_coder(text, build_encoder(j))
	# 	n = t.split()
	# 	if is_word(wordlist, n[0]):
	# 		print n[0]
	# 	j += 1
	return False

s = random_scrambled(wordlist, 25)
#print s
#s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
shifts = find_best_shifts(wordlist, s)
#shifts = find_best_shifts(wordlist, 'kyfukduvertlnvmhgbwtxyiux syfjk vjiuxlcbcihmubvzerysmzrfbtnkgtcph iccqmfbetwqtpihdomwwxwsumjxppawieopucqoedlmbocloyqloxultwmtbock yrhmyltbgxqovivahnnxjgejcwhxiznxrdmefvctaebufmjofeanxnyhaevaowirgosgtzfvuurbnwnaa')
print shifts

def decrypt_fable():
	text = get_fable_string()
	print find_best_shifts(wordlist, text)


#decrypt_fable()
#What is the moral of the story?
#
#
#
#
#
