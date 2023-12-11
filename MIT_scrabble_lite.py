import sys
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}
#I wanted to add a limit to the number of plays based on the number of tiles the game offered. 
TILES = [
    'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'D', 'D', 'E', 'E', 'E', 'E', 'E',
    'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'F', 'F', 'G', 'G', 'G', 'H', 'H', 'I', 'I', 'I', 'I', 'I', 'I', 'I',
    'I', 'I', 'J', 'K', 'L', 'L', 'L', 'L', 'M', 'M', 'N', 'N', 'N', 'N', 'N', 'N', 'O', 'O', 'O', 'O', 'O', 'O',
    'O', 'O', 'P', 'P', 'Q', 'R', 'R', 'R', 'R', 'R', 'R', 'S', 'S', 'S', 'S', 'T', 'T', 'T', 'T', 'U', 'U', 'U',
    'U', 'V', 'V', 'W', 'W', 'X', 'Y', 'Y', 'Z'
]

WORDLIST_FILENAME = "words.txt"


def loadWords(filename):
    try:
        with open(filename, 'r') as file:
            return [word.strip().upper() for word in file]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)


def calculateHandlen(hand):
    if isinstance(hand, list):
        return len(hand)
    elif isinstance(hand, dict):
        return sum(hand.get(keysV, 0) for keysV in hand)
    else:
        raise TypeError("Unsupported type for hand: {}".format(type(hand)))


def displayHand(hand):
    for letter in hand:
        print(letter, end='')
    print()


def dealHand(n, tiles_left):
    hand = []

    for _ in range(n):
        if not tiles_left:
            break  # If there are no more tiles, exit the loop
        random_tile = random.choice(tiles_left)
        hand.append(random_tile)
        tiles_left.remove(random_tile)

    return hand


def updateHand(hand, word):
    updatedHand = hand.copy()
    for letter in word:
        if letter in updatedHand:
            updatedHand.remove(letter)
    return updatedHand


def isValidWord(word, hand, wordList):
    hand2 = hand.copy()
    wordListCheck = True
    letterInKeysCheck = False
    for letter in word:
        wordCheck = hand2.count(letter)
        if letter in hand2 and wordCheck == 0:
            letterInKeysCheck = False
            break
        elif letter in hand2 and wordCheck != 0:
            hand2.remove(letter)
            letterInKeysCheck = True

    if wordListCheck == True and letterInKeysCheck == True:
        return True
    else:
        return False


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
                print("User ended game. Your total score was " + str(totalScore))
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


def playGame(wordList, tiles):
    while True:
        answer3 = input("Enter 'e' to exit. Enter 'n' for a new hand. Enter 'r' for your previous hand: ")
        if answer3 == 'e':
            print("You are exiting the game.")
            break
        elif answer3 == 'n' or answer3 == 'r':
            playHand(wordList, HAND_SIZE, tiles)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py words.txt")
        sys.exit(1)

    wordList = loadWords(sys.argv[1])
    playGame(wordList, TILES)
