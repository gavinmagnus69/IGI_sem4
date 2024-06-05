def try_again() -> bool:
    print("\nWould you like to try again?")
    print("1 - YES")
    print("anything except 1 - NO")
    ans = input("your choice is: ")
    if ans == "1":
        return True
    else:
        return False