# Project 2: Simple Calculator

In this project, we'll build a basic calculator. This will introduce you to a few new, important concepts:

1.  **Working with Numbers:** We'll learn how to handle numerical input.
2.  **Type Casting:** The `input()` function gives us text (a "string"). We'll learn to convert that text into a number using `float()`.
3.  **Conditional Logic:** We'll use `if`, `elif` (else if), and `else` statements to decide which mathematical operation to perform based on the user's input.

## Code

```python
# 1. Get the first number from the user
num1 = float(input("Enter the first number: "))

# 2. Get the operator from the user
op = input("Enter an operator (+, -, *, /): ")

# 3. Get the second number from the user
num2 = float(input("Enter the second number: "))

# 4. Perform the calculation
if op == "+":
    result = num1 + num2
elif op == "-":
    result = num1 - num2
elif op == "*":
    result = num1 * num2
elif op == "/":
    result = num1 / num2
else:
    result = "Invalid operator"

# 5. Print the result
print(f"The result is: {result}")
```

## How to Run the Code

1.  Open a terminal or command prompt.
2.  Navigate to the `2_simple_calculator` directory.
3.  Run the script using the command: `python3 main.py`
