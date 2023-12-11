import sys
import random
import string

# Code given by the assignment:

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# For my version of the game, I wanted to give a limit to the letters used.
# So I added the Tiles with the amount of letters I wanted to have.

TILES = [
    'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'D', 'D', 'E', 'E', 'E', 'E', 'E',
    'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'F', 'F', 'G', 'G', 'G', 'H', 'H', 'I', 'I', 'I', 'I', 'I', 'I', 'I',
    'I', 'I', 'J', 'K', 'L', 'L', 'L', 'L', 'M', 'M', 'N', 'N', 'N', 'N', 'N', 'N', 'O', 'O', 'O', 'O', 'O', 'O',
    'O', 'O', 'P', 'P', 'Q', 'R', 'R', 'R', 'R', 'R', 'R', 'S', 'S', 'S', 'S', 'T', 'T', 'T', 'T', 'U', 'U', 'U',
    'U', 'V', 'V', 'W', 'W', 'X', 'Y', 'Y', 'Z'
]

WORDLIST_FILENAME = "words.txt"

# I wanted the game to run from the command line so I had to make a couple of changes.

def loadWords(filename):
    try:
        with open(filename, 'r') as file:
            return [word.strip().lower() for word in file]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

# I wonder if there is a Scrabble library that I can import and would be updated instead of a txt doc.

def getFrequencyDict(sequence):
    freq = {}  # Initializes an empty dictionary to store the frequencies.
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq

# This function is to show how many letters a given word has and used.
# E.g., EGG - There are 12 'e' in the bag, and only 3 'g' so if you write egg, you should only have one g left and 11 'e' left.
# Uncomment the code below to test the function.
# result_str = getFrequencyDict("hello")
# print(result_str)

### Code that I had to produce:

# 1 - Def getWordScore(word, n):

def getWordScore(word, n):
    wordScore = sum(SCRABBLE_LETTER_VALUES[letter.lower()] for letter in word)
    if len(word) == n:
        wordScore += 50

    return wordScore

# This function calculates the score of a word, it will check each letter in the word, and check the value of that letter.
# then it will calculate how much it is worth. If a word used all 7 letters of the hand, then the user gets another 50 points.


# 2 - Def displayHand(hand)
# This function will display the hand the user currently has.

def displayHand(hand):
    for letter in hand:
        print(letter, end='')  # print all in one line
    print()  # adding this so it gives a little space
    print()


# 3 def dealHand

def dealHand(n, tiles_left):
    hand = {}
    numVowels = n // 3  # 1/3 of the hand letters must be a vowel.

    for i in range(numVowels):
        if not tiles_left:
            break  # If there are no more tiles, exit the loop
        random_tile = random.choice(tiles_left)
        hand[random_tile] = hand.get(random_tile, 0) + 1
        tiles_left.remove(random_tile)

    for i in range(numVowels, n):
        if not tiles_left:
            break  # If there are no more tiles, exit the loop
        random_tile = random.choice(tiles_left)
        hand[random_tile] = hand.get(random_tile, 0) + 1
        tiles_left.remove(random_tile)

    return hand


# 4 def updateHand(hand, word)
# the professor explained this case in class. see video.
def updateHand(hand, word):

    updatedHand = hand.copy()  # I learned to make a copy of the hand.
    # So it won't change the main one
    for letter in word:
        if letter in updatedHand:
            updatedHand[letter] -= 1  # So if my original hand had 7 letters: h a a d p p y - and I use HAPPY, my updated hand will A D.
            if updatedHand[letter] == 0:  # This will remove the letter from the hand if I don't have another, in this case: it will remove HPPY, but keep 1 A, since I had 2
                del updatedHand[letter]
    return updatedHand

# 5 def isValidWord(word, hand, wordList)
# Making sure a word is valid by checking the list.

def isValidWord(word, hand, wordList):
    hand2 = hand.copy()  # making a copy so I don't mess anything up
    wordListCheck = True
    letterInKeysCheck = False

    for letter in word:
        wordCheck = hand2.count(letter)  # counting how many letters.

        if letter in hand2 and wordCheck == 0:
            letterInKeysCheck = False
            break
        elif letter in hand2 and wordCheck != 0:  # Checking if the user hand has the letter in the word inputted.

            hand2.remove(letter)
            letterInKeysCheck = True

        if wordListCheck == True and letterInKeysCheck == True:
            return True

        else:
            return False


# 6 - def playHand

def playHand(wordList, n, tiles):
    totalScore = 0
    tiles_left = tiles.copy()

    while tiles_left:
        hand = dealHand(n, tiles_left)

        while calculateHandlen(hand) > 0:
            print("Your current hand is: ")
            displayHand(hand)
            answer = input("Enter a word with your letters (or '.' to end the game): ")

            if answer == ".":
                print("User ended the game. Your total score was " + str(totalScore))
                return

            if not isValidWord(answer, hand, wordList):
                print("This is not a valid word, please try again.")
            else:
                wordScore = sum(SCRABBLE_LETTER_VALUES[letter.lower()] for letter in answer)
                totalScore += wordScore
                print(f"This word is worth {wordScore}! Your current score is {totalScore}.")
                hand = updateHand(hand, answer)
                print()

        print("No more letters in your hand. Dealing a new hand.")
        tiles_left = [tile for tile in tiles_left if tile not in hand]

    print("No more tiles left. Game over. Your total score was " + str(totalScore))


# 7 - def calculateHandlen(hand)

def calculateHandlen(hand):
    handLength = 0
    for keysV in hand:
        if hand.get(keysV, 0) != 0:
            handLength += hand.get(keysV, 0)

    return handLength


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py words.txt")
        sys.exit(1)

    wordList = loadWords(sys.argv[1])
    playHand(wordList, HAND_SIZE, TILES)
