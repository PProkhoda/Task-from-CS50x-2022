// Implements a dictionary's functionality
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <strings.h>

#include <ctype.h>
#include <stdbool.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 100000;

// Hash table
node *table[N];

//calculate word
int wordcount = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // hash word
    int key = hash(word);
    //create new node
    node *cursor = table [key];
    //compare cursor & hashtable list
    while (cursor != NULL)
    {
        if (strcasecmp((cursor -> word), (table[key] -> word)) == 0)
        {
            return true;
        }
        cursor = cursor -> next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    // Function should take a string and return an index
    // This hash function adds the ASCII values of all characters in     the word together
    long sum = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        sum += tolower(word[i]);
    }
    return sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
//        printf("Could not open %s.\n", dictionary);
        return false;
    }

    //scan to word[]
    char buffer[LENGTH + 1];
    while (fscanf(dict, "%s", buffer) != EOF)
    {

        // try to instantiate node to insert word
        node *newptr = malloc(sizeof(node));
        if (newptr == NULL)
        {
            free(newptr);
            return false;
        }

        // make a new pointer
        strcpy(newptr->word, buffer);
        newptr->next = NULL;

        //hash word
        int key = hash(buffer);

        // insertion at first
        newptr -> next = table[key];
        table[key] = newptr;
        wordcount++;
    }
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // return wordcount
    return wordcount;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO

    for (int i = 0; i < N; i++)
    {
        node *curs = table[i];

        while (curs != NULL)
        {
            // Make temp equal cursor;
            node *tmp = curs;
            // Point cursor to next element
            curs = curs -> next;
            // free temp
            free(tmp);
        }
        if (curs == NULL && i == N - 1)
        {
            return true;
        }
    }
    return false;
}
