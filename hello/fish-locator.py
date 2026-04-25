#!/usr/bin/env python3

import random

# Select a random number between 1 and 10
secret_number = random.randint(1, 10)

while True:
    try:
        guess = int(input("Guess a number (1-10): "))

        if guess == secret_number:
            print("This is where the fish lives.")
            break
        else:
            print("I'm sorry, but your fish is in another lake.")
    except ValueError:
        print("Please enter a valid number.")
