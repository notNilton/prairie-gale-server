# calculations.py

def add_numbers(number_a, number_b, number_c):
    try:
        number_a = float(number_a)
        number_b = float(number_b)
        number_c = float(number_c)
        return number_a + number_b + number_c
    except ValueError:
        raise ValueError("Invalid numbers provided")
