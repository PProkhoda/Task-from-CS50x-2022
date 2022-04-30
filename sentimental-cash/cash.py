from cs50 import get_float


def get_cents():
    while True:
        c = get_float("Change owed: ")
        if c > 0:
            break
    c = c * 100
    return c


def calculate_quarters(cents):
    return cents / 25


def calculate_dimes(cents):
    return cents / 10


def calculate_nickels(cents):
    return cents / 5


def calculate_pennies(cents):
    return cents


def main():
    # Ask how many cents the customer is owed
    cents = get_cents()

    # Calculate the number of quarters to give the customer
    quarters = int(calculate_quarters(cents))
    cents = cents - quarters * 25

    # Calculate the number of dimes to give the customer
    dimes = int(calculate_dimes(cents))
    cents = cents - dimes * 10

    # Calculate the number of nickels to give the customer
    nickels = int(calculate_nickels(cents))
    cents = cents - nickels * 5

    # Calculate the number of pennies to give the customer
    pennies = int(calculate_pennies(cents))
    cents = cents - pennies * 1

    # Sum coins
    coins = quarters + dimes + nickels + pennies

    # Print total number of coins to give the customer
    print("coins ", coins)


main()
