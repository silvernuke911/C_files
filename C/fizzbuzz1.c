#include <stdio.h>
#include <string.h> 

#include <stdio.h>
#include <string.h>

void fizzbuzz1(void) {
    for (int i = 1; i <= 100; i++) {
        char output[16] = "";  // String allocation fucker
        if (i % 3 == 0) {
            strcat(output, "Fizz");
        }
        if (i % 5 == 0) {
            strcat(output, "Buzz");
        }
        if (strlen(output) == 0) {
            printf("%d\n", i);
        } else {
            printf("%s\n", output);
        }
    }
}

void fizzbuzz2(void) {
    for (int i = 1; i <= 100; i++) {
        if ((i % 3 == 0)&&(i % 5 == 0)) {
            printf("Fizzbuzz\n");
        } else if (i % 3 == 0) {
            printf("Fizz\n");
        } else if (i % 5 == 0) {
            printf("Buzz\n");
        } else {
            printf("%i\n", i); 
        }
    }
}

int main(void){
    fizzbuzz1();
    printf("====SECOND VERSION===\n");
    fizzbuzz2();
    return 0;
}