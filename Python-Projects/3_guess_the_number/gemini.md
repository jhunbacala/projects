# Project 3: Guess the Number Game

This project is a classic programming exercise and a lot of fun. We'll build a game where the computer thinks of a number and the user has to guess it.

This will introduce two powerful new concepts:

1.  **Importing Modules:** Python has a huge standard library of code that you can use. We'll `import` the `random` module to generate a random number.
2.  **`while` Loops:** We'll use a `while` loop to allow the user to keep guessing until they get the right answer. A `while` loop continues to run as long as a certain condition is true.
3.  **Error Handling:** We'll use a `try...except` block to gracefully handle cases where the user enters something that isn't a number.
4.  **Breaking Loops:** We'll use the `break` keyword to exit our loop once the user guesses correctly.

## Code

```python
import random

# 1. Generate a random number between 1 and 100
secret_number = random.randint(1, 100)
print("I'm thinking of a number between 1 and 100.")

# 2. Start the game loop
while True:
    # 3. Get the user's guess
    try:
        guess = int(input("What's your guess? "))
    except ValueError:
        print("Please enter a valid number.")
        continue

    # 4. Compare the guess to the secret number
    if guess < secret_number:
        print("Too low! Try again.")
    elif guess > secret_number:
        print("Too high! Try again.")
    else:
        print(f"You got it! The number was {secret_number}.")
        break # Exit the loop
```

## How to Run the Code

1.  Navigate to the `3_guess_the_number` directory.
2.  Run the script: `python3 main.py`
