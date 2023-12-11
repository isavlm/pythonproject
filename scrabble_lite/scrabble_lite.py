import sys
import time
import random

#First working on my main screen
def printing_scrabble_art():
    try:
        with open('ascii_art.txt', 'r') as art_file:
            art = art_file.read()
            print(art)
    except FileNotFoundError:
        print("Error: ASCII art file not found.")
        sys.exit(1)

    time.sleep(2)

def main():
    if len(sys.argv) != 2:
        print("Usage: python your_scrip.py word_file.txt")
        sys.exit(1)

    word_file = sys.argv[1]


    # Start the game and loading page
    printing_scrabble_art()

    # Create an instance of TextScrabble with the provided word file
    scrabble_game = TextScrabble(word_file)

    # Play the game
    scrabble_game.play_game()


if __name__ == "__main__":
    main()

