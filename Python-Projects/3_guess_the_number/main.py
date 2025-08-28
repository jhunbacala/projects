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
