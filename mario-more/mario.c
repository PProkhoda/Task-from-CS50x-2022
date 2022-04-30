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
        for (int j = 0; j < 2 * h + 2; j++)
        {
            //print а "space"
            if (j < h - 1 - i)
            {
                printf(" ");
            }
            //print brick
            else if (j < h)
            {
                printf("#");
            }
            //print double spase
            else if (j < h + 2)
            {
                printf(" ");
            }
            //print last brick
            else if (j < h + 3 + i)
            {
                printf("#");
            }
        }
        //move to next row
        printf("\n");
    }
}
