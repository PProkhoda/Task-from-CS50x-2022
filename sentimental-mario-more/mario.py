from cs50 import get_int

while True:
    h = get_int("Heyght: ")
    if h > 0 and h < 9:
        break

for i in range(h):
    for j in range(2 * h + 2):

        # print а "space"
        if j < (h - 1 - i):
            print(" ", end="")

        # print brick
        elif j < h:
            print("#", end="")

        # print double spase
        elif j < (h + 2):
            print(" ", end="")

        # print last brick
        elif j < (h + 3 + i):
            print("#", end="")
    print()
