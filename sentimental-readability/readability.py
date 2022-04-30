from cs50 import get_string


def count_letters(text):
    scoreletters = 0
    for char in text:
        if char.isalpha():
            scoreletters += 1
    return scoreletters


def count_words(text):
    scorewords = 1
    for char in text:
        char = ord(char)
        if char == 32:
            scorewords += 1
    return scorewords


def count_sentences(text):
    sentences = 0
    for char in text:
        char = ord(char)
        if char == 46:
            sentences += 1
        elif char == 33:
            sentences += 1
        elif char == 63:
            sentences += 1
    return sentences


def main():
    # enter text
    text = get_string("Text: ")

    # calculation of the number of letters
    letters = count_letters(text)
    print("L", letters)

    # calculation of the number of words
    words = count_words(text)
    print("W", words)

    # calculation of the number of sensetenses
    sentences = count_sentences(text)
    print("S", sentences)

    L = (letters / words) * 100
    print(L)
    S = (sentences / words) * 100
    print(S)
    # calculate Coleman-Liau index
    index1 = (0.0588 * L) - (0.296 * S) - 15.8
    index = round(index1)

    # print "Grade 16+"
    if index > 16:
        print("Grade 16+")

    # print "Before Grade 1"
    elif index < 1:
        print("Before Grade 1")

    # print "Grade index"
    else:
        print("Grade ", index)


main()

