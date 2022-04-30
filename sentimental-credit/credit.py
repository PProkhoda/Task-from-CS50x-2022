from cs50 import get_int


# 10 to the power of n
def Pow(n):
    res = 1
    for i in range(n):
        res *= 10
    return res


def main():
    while True:
        number = get_int("Number: ")
        if number > 0:
            break
    # calculation of digit capacity of a number
    w = len(str(number))

    # first subtotal
    sum1 = 0
    for n in range(2, w + 1, 2):

        # determining the number for the subsequent calculation of the checksum
        z = int(((number % Pow(n)) - (number % Pow(n - 1))) / (Pow(n - 1)))
        x = int(((z * 2) % 100 / 10) + ((z * 2) % 10))
        sum1 = sum1 + x

    # second subtotal
    sum2 = 0
    for n in range(1, w + 1, 2):
        # determining the number for the subsequent calculation of the checksum
        z = int(((number % Pow(n)) - (number % Pow(n - 1))) / (Pow(n - 1)))

        x = int(((z) % 100 / 10) + ((z) % 10))
        sum2 = sum2 + x

    controldigits = int((number - number % Pow(w - 2)) / Pow(w - 2))
    controldigitsvisa = int((number - number % Pow(w - 1)) / Pow(w - 1))
    controlsum = sum1 + sum2

    if controlsum % 10 == 0:
        # Validate American Express
        if w == 15:
            if controldigits == 34 or controldigits == 37:
                print("AMEX")
            else:
                print("INVALID")

        # Validate MasterCard
        elif w == 16:
            if controldigits == 51 or controldigits == 52 or controldigits == 53 or controldigits == 54 or controldigits == 55:
                print("MASTERCARD")
            # Validate Visa
            elif controldigitsvisa == 4:
                print("VISA")
            else:
                print("INVALID")

        # Validate Visa
        elif w == 13:
            if controldigitsvisa == 4:
                print("VISA")
            else:
                print("INVALID")
        else:
            print("INVALID")
    else:
        print("INVALID")


main()
