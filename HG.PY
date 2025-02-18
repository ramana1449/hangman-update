import random
from collections import Counter
import nltk  # For NLTK's word list (if you want to restrict to common words)
try:
    from spellchecker import SpellChecker  # type: ignore # For spell checking
except ImportError:
    print("Spellchecker library not found. Install it using: pip install spellchecker")
    SpellChecker = None

try:
    nltk.download('words', quiet=True)  # Download the NLTK words list (only if needed)
    english_words = set(nltk.corpus.words.words())  # Create a set for faster lookups
except LookupError:
    print("NLTK words list not found. Install it using: nltk.download('words')")
    english_words = None

def play_hangman(use_ai_hint=True, use_spellcheck=True):
    word_list = ["apple", "banana", "orange", "grape", "mango", "pineapple", "watermelon", "strawberry", "blueberry", "raspberry", "kiwi", "apricot", "avocado", "blackberry", "cherry"]  # More fruit options
    word = random.choice(word_list)

    print('Guess the word! HINT: word is a name of a fruit')

    for _ in word:
        print('_', end=' ')
    print()

    letters_guessed = set()
    chances = len(word) + 2
    spell_checker = SpellChecker() if SpellChecker is not None else None  # Initialize spellchecker if available

    while chances > 0:
        print()
        chances -= 1

        while True:  # Input loop to handle invalid or misspelled guesses
            try:
                guess = input('Enter a letter to guess: ').lower()
            except:
                print('Invalid input!')
                continue

            if not guess.isalpha() or len(guess) != 1:
                print('Enter only a SINGLE letter')
                continue

            if guess in letters_guessed:
                print('You have already guessed that letter')
                continue

            if use_spellcheck and spell_checker:
                if spell_checker.unknown([guess]):  # Check for spelling errors
                    correction = spell_checker.correction(guess)
                    if correction != guess:
                        print(f"Did you mean {correction}? (y/n)")
                        confirm = input().lower()
                        if confirm == 'y':
                            guess = correction
                            break  # Exit the inner loop after correction
                        else:
                            continue  # Ask for input again if not confirmed
                    else:
                        break # Correctly spelled, exit input loop
                else:
                    break # Correctly spelled, exit input loop
            else:
                break # Spellcheck disabled, exit input loop

        letters_guessed.add(guess)

        if guess in word:
            print("Good guess!")
        else:
            print("Incorrect guess.")

        word_display = ""
        for char in word:
            if char in letters_guessed:
                word_display += char + " "
            else:
                word_display += "_ "
        print(word_display)

        if all(char in letters_guessed for char in word):
            print("The word is:", word)
            print('Congratulations, You won!')
            return

        if use_ai_hint and chances <= len(word) // 2: # Offer a hint after half the chances are used
            # Basic AI hint: suggests a common letter not yet guessed
            available_letters = [char for char in "aeioulnstr" if char in word and char not in letters_guessed]
            if available_letters:
                hint_letter = random.choice(available_letters)
                print(f"AI Hint: Try guessing the letter '{hint_letter}'.")

    print()
    print('You lost! Try again..')
    print('The word was {}'.format(word))


if __name__ == '__main__':
    while True:
        play_hangman(use_ai_hint=True, use_spellcheck=True)  # Enable AI hint and spellcheck
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            break