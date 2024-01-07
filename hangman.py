import csv
import random
from hangman_stages import HANGMAN_STAGES

MAX_WRONG_ATTEMPTS = 6

def main():
    # Welcome message to the Hangman game
    print("WELCOME TO HANGMAN!")

    # Select a random word from a list of words
    word = choose_word()
    
    # Initialize variables to track the state of the game
    correctlyGuessedIndices = []  # Indices of correctly guessed letters
    guessedLetters = []  # Letters guessed by the player

    # Generate initial underscores for the word
    underscores = get_underscores(word, correctlyGuessedIndices)
    print(underscores)

    # Start the guessing loop and get the results
    wrongAttempts, correctAttempts = guess(word, underscores, correctlyGuessedIndices, guessedLetters)

    # Display the outcome of the game based on the results
    if wrongAttempts == MAX_WRONG_ATTEMPTS:
        print("YOU LOST! The word was", word)
    elif correctAttempts == len(word):
        print("GREAT JOB! The word was", word)


def choose_word():
    # Read a list of words from a CSV file and select a random word
    with open(r"C:\Users\Hasib\Documents\VS Code Projects\Hangman\nounlist.csv", "r") as file:
        reader = csv.reader(file)
        rows = list(reader)
        randomWord = random.choice(rows)
        selectedWord = randomWord[0]
        return selectedWord


def get_underscores(word, correctlyGuessedIndices):
    # Generate a string with underscores representing the word, revealing correct guesses
    display = ""
    for i, letter in enumerate(word):
        if letter == " " or i in correctlyGuessedIndices or letter == "-":
            display += letter
        else:
            display += "_"
    return display


def guess(word, underscores, correctlyGuessedIndices, guessedLetters):
    # Main game loop for handling guesses
    wrongAttempts = 0
    correctAttempts = 0
    while wrongAttempts < MAX_WRONG_ATTEMPTS and correctAttempts < len(word):
        guess = input("\nGuess a letter: ").lower()

        # Check the validity of the guess and update game state
        if check_validity(guess, guessedLetters):
            wrongAttempts, correctAttempts, correctlyGuessedIndices = check_correctness(guess, word, underscores, wrongAttempts, correctAttempts, correctlyGuessedIndices, guessedLetters)

    return wrongAttempts, correctAttempts

def check_validity(guess, guessedLetters):
    # Validate the user's input for a valid guess
    if not guess:
        print("Please enter a letter.")
        return False
    elif len(guess) != 1:
        print("\nEnter one letter at a time!")
        return False
    elif not guess.isalpha():
        print("\nEnter letters only!")
        return False
    elif guess in guessedLetters:
        print("You already guessed that letter! \nLetter bank: ", guessedLetters)
        return False
    return True


def check_correctness(guess, word, underscores, wrongAttempts, correctAttempts, correctlyGuessedIndices, guessedLetters):
    # Check if the guessed letter is correct and update game state accordingly
    if guess in word:
        occurrences = [i for i, letter in enumerate(word) if letter == guess]
        correctlyGuessedIndices.extend(occurrences)
        correctAttempts += len(occurrences)
    else:
        # Incorrect guess, increment wrong attempts and display the hangman stage
        wrongAttempts += 1
        print(HANGMAN_STAGES[wrongAttempts])

    # Update guessed letters, underscores, and display the game state
    guessedLetters.append(guess)
    underscores = get_underscores(word, correctlyGuessedIndices)
    print("\nLetter bank:", guessedLetters)
    print(underscores)
    return wrongAttempts, correctAttempts, correctlyGuessedIndices


main()
