from cs50 import get_int

while True:
    h = get_int("Heyght: ")
    if h > 0 and h < 9:
        break

for i in range(h):
    for j in range(h):

        # print а "space"
        if j < (h - 1 - i):
            print(" ", end="")

        # print а "brick"
        else:
            print("#", end="")
    print()
