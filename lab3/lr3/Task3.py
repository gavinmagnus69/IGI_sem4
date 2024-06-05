import prints

def if_hexadecimal(s : str) -> bool:
    '''
           this function checs if given sstring is hexidecimal number or not
    '''
    try:
        numero = int(s, 16)
        return True
    except ValueError:
        return False
            


def main():
    while True:
        print("\nThis task checks if your string is hexadecimal or not")
        your_str = input("enter your string: ")
        flag = if_hexadecimal(your_str)

        if flag:
            print("your string is hexadecimal number")
        else:
            print("your string is not hexadecimal number")
        if not prints.try_again():
            break     
        print()

if __name__ == "__main__":
    main()