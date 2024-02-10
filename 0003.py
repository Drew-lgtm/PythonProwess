def is_prime(number):
    if number <= 1:
        return False
    elif number == 3:
        return True
    elif number == 5:
        return True
    elif number == 7:
        return True
    elif number % 2 == 0 or number % 3 == 0 or number % 5 == 0 or number % 7 == 0:
        return False
    else:
        return True

while True:
    number = input("Enter a number (or 'q' to quit): ")
    if number.lower() == 'q':
        break

    try:
        number = int(number)
        if is_prime(number):
            print(number, "is a prime number")
        else:
            print(number, "is NOT a prime number")
    except ValueError:
        print("Invalid input. Please enter a number or 'q' to quit.")