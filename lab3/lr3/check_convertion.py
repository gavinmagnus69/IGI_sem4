def is_valid_int(n) -> bool:
    """
A function to check the validity of the number n.
    Returns True if n is a non-negative integer, and False otherwise.
    """
    try:
        n = int(n)
    except (TypeError, ValueError):
        return False
    return True       
def is_valid_float(n) -> bool:
    """
A function to check the validity of the number n.
    Returns True if n is a non-negative integer, and False otherwise.
    """
    try:
        n = float(n)
    except (TypeError, ValueError):
        return False
    return True            

def valid_input_int(text: str) -> int:
    tmp = input(text)

    while not is_valid_int(tmp):
        print("Invalid input, please, try again:")
        tmp = input()
    return int(tmp)

def valid_input_float(text: str) -> float:
    tmp = input(text)

    while not is_valid_float(tmp):
        print("Invalid input, please, try again:")
        tmp = input()
    return float(tmp)
