import random

from RandomWords import easy_wordlist, medium_wordlist, hard_wordlist

DIFFICULTY_LEVEL = "medium"


def hangman(tries):
    stages = [
        """
                           --------
                           |      |
                           |      O
                           |     \\|/
                           |      ||
                           |     // \\
                           -
                        """,
        """
                           --------
                           |      |
                           |      O
                           |     \\|/
                           |      |
                           |     // \\
                           -
                        """,
        """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """,
        """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """,
        """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """,
        """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """,
        """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """,
        """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """,
        """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """,
    ]
    return stages[tries]

def get_word(difficult):
    DIFFICULTY_LEVEL=difficult
    if DIFFICULTY_LEVEL == "easy":
        word = random.choice(easy_wordlist)
    elif DIFFICULTY_LEVEL == "medium":
        word = random.choice(medium_wordlist)
    elif DIFFICULTY_LEVEL == "hard":
        word = random.choice(hard_wordlist)
    else:
        word = random.choice(medium_wordlist)
    return word.upper()


def choose_difficulty(difficult):
    DIFFICULTY_LEVEL = difficult
    if DIFFICULTY_LEVEL == "easy":
        return (
            8  # we can adjust the number of initial guesses for each difficulty level
        )
    elif DIFFICULTY_LEVEL == "medium":
        return 6
    elif DIFFICULTY_LEVEL == "hard":
        return 4
    else:
        print("Invalid difficulty level. Defaulting to medium.")
        return 6


def play(word, initial_tries):
    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []

    tries = initial_tries

    print("\n-------------Welcome to Hangman-------------\n")
    print(hangman(tries))
    print(word_completion)
    print("\n")
    while not guessed and tries > 0:
        guess = input("Guess the word:- ").upper()
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You already guessed the letter", guess)
            elif guess not in word:
                print(guess, "is not in the word.")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print("Good job,", guess, "is in the word!")
                guessed_letters.append(guess)
                word_as_list = list(word_completion)
                indices = [i for i, letter in enumerate(word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                word_completion = "".join(word_as_list)
                if "_" not in word_completion:
                    guessed = True

        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print("You already guessed the word", guess)
            elif guess != word:
                print(guess, "is not the word.")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word

        else:
            print("An incorrect guess.")
        print(hangman(tries))
        print(word_completion)
        print("\n")

    if guessed:
        print("Congrats, you guessed the word! You win!")

    else:
        print("Sorry, you ran out of tries. The word was " + word + ". play again :)")


def main():
    """
    * This triggers the game by asking for intialization
    """
    global DIFFICULTY_LEVEL
    DIFFICULTY_LEVEL = input("Choose difficulty level (easy, medium, hard): ").lower()
    difficulty = choose_difficulty(DIFFICULTY_LEVEL)
    word = get_word(difficulty)
    play(word, difficulty)
    while input("Do you want to play Hangman? (y/n): ").upper() == "Y":
        difficulty = choose_difficulty()
        word = get_word()
        play(word, difficulty)


if __name__ == "__main__":
    main()
