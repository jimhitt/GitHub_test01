import random
import csv
import random

def load_word_list(file_path):
    words = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            words.extend(row)  # Adds all words in this row to the list
    return words

def choose_secret_word(word_list):
    # Randomly choose a secret word
    return random.choice(word_list)

def get_user_guess(valid_words=None, word_length=5):
    # Get a valid guess from the user
    while True:
        guess = input(f"Enter a {word_length}-letter word: ").strip().upper()

        # Check if the guess is the correct length
        if len(guess) != word_length:
            print(f"Please enter a word with exactly {word_length} letters.")
            continue

        # If a list of valid words is provided, check if the guess is in the list
        if valid_words is not None and guess not in valid_words:
            print("Invalid word. Please enter a different word.")
            continue

        return guess


def compare_guess_with_secret(guess, secret):
    # Compare the guess with the secret word and provide feedback
    feedback = [None for _ in range(len(secret))]

    # Copy of secret to mark letters that have been matched
    secret_copy = list(secret)

    # First pass: check for correct letters in the correct positions
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            feedback[i] = '+'  # Symbol for correct position
            secret_copy[i] = None  # Mark this letter as matched

    # Second pass: check for correct letters in wrong positions
    for i in range(len(guess)):
        if guess[i] != secret[i]:
            if guess[i] in secret_copy:
                feedback[i] = '-'  # Symbol for wrong position
                secret_copy[secret_copy.index(guess[i])] = None  # Mark this letter as matched
            else:
                feedback[i] = '*' # Symbol for not in the word

    return ''.join(feedback)


def display_results(guesses, feedbacks):
    # display the results (must pass a list)
    # ANSI Color Codes
    GREEN = "\033[32m"  # Correct position
    YELLOW = "\033[33m" # Wrong position
    GRAY = "\033[90m"   # Not in the word
    RESET = "\033[0m"   # Reset to default color
    i = 1
    for guess, feedback in zip(guesses, feedbacks):
        colored_output = ""
        for char, fb in zip(guess, feedback):
            if fb == '+':
                color = GREEN
            elif fb == '-':
                color = YELLOW
            else:
                color = GRAY
            colored_output += color + char + RESET + ' '
        print(str(i), ': ', colored_output)
        print()  # New line for separation
        i += 1

def main():
    word_list = load_word_list("words_5_letter.csv")
    secret_word = choose_secret_word(word_list).upper()
    attempts = 6
    guesses = []
    feedbacks = []

    while attempts > 0:
        guess = get_user_guess()
        if not guess:
            continue
        guesses.append(guess)
        feedback = compare_guess_with_secret(guess, secret_word)
        feedbacks.append(feedback)
        display_results(guesses, feedbacks)
        if guess == secret_word:
            print("Congratulations! You guessed the word!")
            break
        attempts -= 1

    if attempts == 0:
        print(f"Game Over! The secret word was {secret_word}.")

if __name__ == "__main__":
    main()
