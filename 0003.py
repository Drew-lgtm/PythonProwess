def is_number_prime(number):

    if type(number) == float:
        return False

    if number <= 1:
        return False

    if number <= 3:
        return True

    if number % 2 == 0 or number % 3 == 0:
        return False

    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6

    return True

"""while True:
    number = input("Enter a number (or 'q' to quit): ")
    if number.lower() == 'q':
        break

    try:
        number = int(number)
        if is_number_prime(number):
            print(number, "is a prime number")
        else:
            print(number, "is NOT a prime number")
    except ValueError:
        print("Invalid input. Please enter a number or 'q' to quit.")"""

main_number = 13195

def prime_factors(main_number = 13195):
    for i in range(main_number):
        colon = main_number - i
        if is_number_prime(colon):
            if is_number_prime(main_number %  colon) and is_number_prime(main_number / colon):
                print(colon)

prime_factors(main_number)
