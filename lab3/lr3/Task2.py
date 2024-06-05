import check_convertion as check
import prints
def count_positives() -> int:
    '''
        Takes integers and calculates the count of positive numbers.
    '''

    count = 0
    while True:
        num = check.valid_input_int("Enter integer number, (enter 10 to finish): ")
        if num == 10:
            break
        if num > 0:
            count += 1
    return count

def main():
    print("this task counts positive integers in sequence")
    cnt = count_positives()
    print(f"There are {cnt} positive integers")
    prints.try_again()


