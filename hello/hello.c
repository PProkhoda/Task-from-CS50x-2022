#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //name prompt
    string name = get_string("Enter your name: ");
    //print hello "name"
    printf("hello, %s\n", name);
}