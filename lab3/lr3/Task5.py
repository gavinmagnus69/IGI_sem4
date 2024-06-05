import generator
import prints
import check_convertion as check

sorted(arr)

def find_max(nums: list) -> int:
    '''
          Function to find maximum absolute value in list
          :parameter
            nums: list
          :return
            max: int
    '''
    if abs(max(nums)) >= abs(min(nums)):
        return abs(max(nums))
    return abs(min(nums))    

def sum_last_positive(nums: list) -> int:
    '''
          Function that sums elements of the list from first to last positive
          :parameter
            nums: list
          :return
            ans: int
    '''

    #1 0 -5 -3 2 -1 -3
    ans = 0
    tmp_sum = 0
    for i in nums:
        tmp_sum += i
        if i > 0:
            ans += tmp_sum
            tmp_sum = 0
    return ans



def choose_generate_method(len: int) -> list:
    '''
          Choise which generate list method use and generate list.
          :parameter
            len(int): count of element in list
          :return
            generated list
    '''
    gen_list = []
    while True:
        method = check.valid_input_int("Enter method of generation: "
        "\n1 - yield generation"
        "\n2 - for generation"
        "\n3 - random generation: ")
        match method:
            case 1:
                for i in generator.generate_yield(len):
                    gen_list.append(i)
            case 2:
                gen_list = generator.generate_list(len)
            case 3:
                gen_list = generator.generate_random(len)
            case _:
                print("Incorrect input\n")
                continue
        break
    return gen_list                


def main():
    while True:
        ln = check.valid_input_int("enter num of elements of list to generate: ")
        gen_list = choose_generate_method(ln)
        print(gen_list)
        mx = find_max(gen_list)
        print(f"absolute maximum eleemnt: {mx}")
        sum_pos = sum_last_positive(gen_list)
        print(f"sum until last positive element(included): {sum_pos}")
        print()
        if not prints.try_again():
            break

if __name__ == "__main__":
    main()    