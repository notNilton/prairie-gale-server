# calculations.py

def add_numbers(number_a, number_b):
    try:
        number_a = float(number_a)
        number_b = float(number_b)
        return number_a + number_b
    except ValueError:
        raise ValueError("Invalid numbers provided")
