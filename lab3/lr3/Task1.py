#ln(1 + x) = sum((-1)^(n-1) x^n / n) |x| < 1
import check_convertion as check
import math
import prints

default_eps = 1e-6
max_iterations = 500


def my_decorator(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print("args:", args)
        print("result:", res)
        return res

    return wrapper





def power(base, pow):
    """
A function for raising the base number to exponent.
    """
    return base ** pow

@my_decorator
def ln_series(x, eps = default_eps):
    """
    Function to compute the value of ln(1 + x) using power series expansion.
    """
    if x == 0:
        return 0
    n = 1
    result = 0
    prev = 0
    while n <= max_iterations:
        prev = result
        result += power(-1, n - 1) * power(x, n) / n

        n += 1
        if abs(prev - result) < eps:
            break
    if n > max_iterations:
        return None, None    
    return result, n



def main():
    while True:
        print()
        
        while True:
            x = check.valid_input_float("Enter x, |x| < 1: ")
            if abs(x) >= 1:
                print("x should be |x| < 1")
            else:
                break    

        my_result, n = ln_series(x)
        math_result = math.log(1 + x)

        if my_result is None:
            print("Too many iterations")
        else:
            print("\nRESULTS:")
            print(f"x = {x}")
            print(f"n = {n}")
            print(f"F(x) = {my_result}")
            print(f"Math F(x) = {math_result}")
            print(f"eps = {default_eps}")
       
        if not prints.try_again():
               break     



if __name__ == "__main__":
    main()