#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h;
    do
    {
        // pyramid height query
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8);

    // for each row
    for (int i = 0; i < h; i++)
    {

        // for each column
        for (int j = 0; j < h; j++)
        {
            //print а "space"
            if (j < h - 1 - i)
            {
                printf(" ");
            }
            //print а "brick"
            else
            {
                printf("#");
            }
        }
        //move to next row
        printf("\n");
    }
}
