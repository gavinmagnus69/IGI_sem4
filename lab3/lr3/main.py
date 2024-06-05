import math

def print_hello():
    print("Lab 3 Akhmetov Roman group 253502\nTask 1: Сalculating the value of a function through a Taylor series with a given accuracy\n"
        "Task2: Organize a loop that takes integers and calculates the arithmetic mean of even numbers. End - input 1\n"
        "Task3: In a string entered from the keyboard, count the number of words starting with a lowercase letter\n"
        "Task4: a) determine the number of words in a line; b) find the longest word and its serial number; c) print every odd word\n"
        "Task5: Find the sum of the negative elements of a list and the product of the elements located between the maximum and minimum elements\n")

def print_menu():
    print("Choose a task:")
    print("1. Task1")
    print("2. Task2")
    print("3. Task3")
    print("4. Task4")
    print("5. Task5")
    print("0. Exit")
    




def main():
    '''
        Main function, the entry point of the program.
    '''
    print_hello()

    while True:
        print_menu()

        choice = input("Enter task num (0-5): ")
        
        if choice == "1":
            import Task1
            print("Task1:")
            Task1.main()
        elif choice == "2":
            import Task2
            print("Task2:\n") 
            Task2.main()
        elif choice == "3":
            import Task3
            print("Task3:\n")
            Task3.main()
        elif choice == "4":
            import Task4
            print("Task4:\n")
            Task4.main()
        elif choice == "5":
            import Task5
            print("Task5:\n")
            Task5.main()
        elif choice == "0":
            print("Exit program")
            break
        else:
            print("Incorrect input. Please, try again\n")


if __name__ == "__main__":
    main()    