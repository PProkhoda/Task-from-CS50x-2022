#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;
const int HEADER_SIZE = 4;

int main(int argc, char *argv[])
{
    // Check for invalid usage
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
//    BYTE *buffer = malloc(512 * 8);
    BYTE buffer[512];

//open file
    FILE *input = fopen(argv[1], "r");
    if (!input)
    {
        return 1;
    }
    int BLOCK_SIZE;

    int count_jpg = 0;
//create new file
    FILE *picture = NULL;
//array of filename.jpg
    char filename[8];

//for first ore anover find *.jpg
    int jpg_start = 0;

    while (fread(buffer, 512, 1, input) == 1)
    {

        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xe0) == 0xe0)
        {
            //not first *.jpg
            if (jpg_start == 1)
            {
                fclose(picture);
            }
            //find first *.jpg
            else
            {
                jpg_start = 1;
            }

            //calculate new name for *.jpg
            sprintf(filename, "%03i.jpg", count_jpg);
            picture = fopen(filename, "w");
            count_jpg++;
        }
        // write to *.jpg
        if (jpg_start == 1)
        {
            fwrite(&buffer, 512, 1, picture);
        }
    }

    fclose(input);
    fclose(picture);
//    free(buffer);
    return 0;
}