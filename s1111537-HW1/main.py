from math_op import *

OPERATIONS = {
    "add": basic_op.add,
    "subtract": basic_op.subtract,
    "multiply": basic_op.multiply,
    "divide": basic_op.divide,
    "average": advanced_op.average,
    "power": advanced_op.power,
    "sqrt": advanced_op.sqrt,
    "log": advanced_op.log
}

operation_idx = [op for op in OPERATIONS.keys()]

while True:
    try:

        print("Please select an operation:")
        for idx,op in enumerate(OPERATIONS):
            print(idx+1,':',op)
        print("0 : Exit or Press Ctrl+C")
        selected_op = input()

        if selected_op == '0':
            break

        if not selected_op.isdigit():
            raise ValueError("Please enter a number")
        
        selected_op = int(selected_op)

        if selected_op < 0 or selected_op > len(OPERATIONS):
            raise ValueError("Please enter a valid number")
        
        selected_op = operation_idx[selected_op-1]

        if selected_op in ["add", "subtract", "multiply", "divide"]:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            print(f"Result: {OPERATIONS[selected_op](a,b)}")

        elif selected_op in ["average"]:
            numbers = input("Enter numbers separated by space: ")
            numbers = [float(num) for num in numbers.split()]
            print(f"Result: {OPERATIONS[selected_op](*numbers)}")

        elif selected_op in ["power","log"]:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            print(f"Result: {OPERATIONS[selected_op](a,b)}")
        
        elif selected_op in ["sqrt"]:
            a = float(input("Enter number: "))
            print(f"Result: {OPERATIONS[selected_op](a)}")

    except KeyboardInterrupt:
        print("Exiting program")
        exit(0)

    except ValueError as e:
        print(f"Get raise error: {e}")
        print("Please Try again.")

    except ZeroDivisionError as e:
        print(f"Get raise error: {e}")
        print("Please Try again.")