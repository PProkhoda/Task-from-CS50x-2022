#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

bool dif_letters(string letters);

int main(int argc, string argv[])
{
    //how many arg entered
    if (argc != 2)
    {
        printf("Usage: 1 key\n");
        return 1;
    }
// check key
    if (strlen(argv[1]) != 26)
    {
        printf("Usage: input 26 letters\n");
        return 1;
    }

    string enteredstring = argv[1];

    if (dif_letters(enteredstring) == false)
    {
        printf("Usage: different letters4\n");
        return 1;
    }
    for (int i = 0; i < 26; i++)
    {
        if (isupper(enteredstring[i]))
        {
        if (dif_letters(enteredstring) == false)
        {
            printf("Usage: different letters4\n");
            return 1;
        }
        }
        else if(islower(enteredstrig[i]))




    char key[26];



}
// check key
bool dif_letters(string letters)
{
    bool list = 0;
    for (int i = 0; i < 26; i++)
    {
        //is all letters differents?
        if (isalpha(letters[i]))
        {
            for (int j = 0; j < i; j++)
            {
                char J = letters[j];
                char I = letters[i];
                if (letters[i] == letters[j])
                {
                    list = false;
//                    printf("Usage: different letters1\n");
                    break;
                }
                else list = true;
            }

            for (int k = 26; k > i; k--)
            {
                char K = letters[k];
                char I = letters[i];
                if (letters[i] == letters[k])
                {
                    list = false;
//                    printf("Usage: different letters2\n");
                    break;
                }
                else
                {
                    list = true;
                }
            }
        }

        else list = false;
        break;
    }
    return list;
}