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
