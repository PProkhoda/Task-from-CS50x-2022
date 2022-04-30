#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>


int count_letters(string text1);

int count_words(string text1);

int count_sentences(string text1);

int main(void)
{
    //enter text
    string text = get_string("Text: ");
    //calculation of the number of letters
    float letters = count_letters(text);
    //calculation of the number of words
    float words = count_words(text);
    //calculation of the number of sensetenses
    int sentences = count_sentences(text);
    double L = (letters / words) * 100;
    double S = (sentences / words) * 100;
    //calculate Coleman-Liau index
    double index1 = (0.0588 * L) - (0.296 * S) - 15.8;
    int index = round(index1);
    //print "Grade 16+"
    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    //print "Before Grade 1"
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    //print "Grade index"
    else
    {
        printf("Grade %i\n", index);
    }

}
//calculation of the number of letters
int count_letters(string text1)
{
    int scoreletters = 0;
    for (int i = 0, n = strlen(text1); i < n; i++)
    {
        if (isalpha(text1[i]))
        {
            scoreletters ++;
        }
    }
    return scoreletters;
}
//calculation of the number of words
int count_words(string text1)
{
    int scorewords = 0;
    for (int i = 0, n = strlen(text1); i < n; i++)
    {
        //word definition
        if (isalpha(text1[i - 1]))
        {
            if (text1[i] == 32)
            {
                scorewords ++;
            }
            else if (text1[i] == 33)
            {
                scorewords ++;
            }
            else if (text1[i] == 44)
            {
                scorewords ++;
            }
            else if (text1[i] == 46)
            {
                scorewords ++;
            }
            else if (text1[i] == 63)
            {
                scorewords ++;
            }
            else if (text1[i] == 58)
            {
                scorewords ++;
            }
            else if (text1[i] == 59)
            {
                scorewords ++;
            }
        }
    }
    return scorewords;
}
//calculation of the number of sensetenses
int count_sentences(string text1)
{
    int sentences = 0;
    for (int i = 0, n = strlen(text1); i < n; i++)
    {
        //sentences definition
        if (isalpha(text1[i - 1]))
        {
            if (text1[i] == 33)
            {
                sentences ++;
            }
            else if (text1[i] == 46)
            {
                sentences ++;
            }
            else if (text1[i] == 63)
            {
                sentences ++;
            }
        }
    }
    return sentences;
}
