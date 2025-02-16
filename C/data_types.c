#include <stdio.h>
#include <stdbool.h>  // Required for bool
#include <string.h>

int main() {
    int x = 1;                          // Integer, 4 bytes (32-bit)         %d or %i
    char a = 'C';                       // Single character, 1 byte          %c
    char b[] = "Hello!";                // String (char array)               %s
    float c = 3.141592;                 // Floating point, 4 bytes (32-bit)  %f
    double d = 3.14159265358979;        // Double, 8 bytes (64-bit)          %lf
    bool e = true;                      // Boolean, 1 byte (true/false)      %d (prints 1 or 0)
    short f = 100;                      // Short integer, 2 bytes (16-bit)   %hd
    long g = 100000L;                   // Long integer, 4 or 8 bytes        %ld
    long long h = 123456789012345LL;    // Long long, 8 bytes                %lld
    unsigned int i = 42;                // Unsigned integer, 4 bytes         %u
    unsigned long j = 123456789UL;      // Unsigned long                     %lu
    unsigned char k = 255;              // Unsigned char, 1 byte             %u
    unsigned short l = 213;             // Unsiged short, 2 bytes            %d     
                                        // %.lf = l decimal precision
                                        // %l   = l minimum field width
                                        // %-   = l left align
    const float pi = 3.141592654;       // constant = fixed value that cannot be altered by the program

    printf("Integer: %d\n", x);
    printf("Character: %c\n", a);
    printf("String: %s\n", b);
    printf("Float: %.6f\n", c);
    printf("Double: %.15lf\n", d);
    printf("Boolean: %d\n", e);
    printf("Short: %hd\n", f);
    printf("Long: %ld\n", g);
    printf("Long Long: %lld\n", h);
    printf("Unsigned Int: %u\n", i);
    printf("Unsigned Long: %lu\n", j);
    printf("Unsigned Char: %u\n", k);
    printf("Constant     : %f\n", pi);

    // Arithmetic operators
    // +  addition
    // -  subtraction
    // *  multiplication
    // /  division
    // %  modulus
    // ++ increment
    // -- decrement

    int w = 24;
    int  y = 20;
    int z = w + y;
    printf("Result + = %i\n", z);
    z = w - y;
    printf("Result - = %i\n", z);
    z = w * y;
    printf("Result * = %i\n", z);
    float m = w / (float) y;
    printf("Result / = %f\n", m);
    z = w % y;
    printf("Result %% = %i\n", z);
    w++;
    printf("Result ++ = %i\n", w);
    y--;
    printf("Result -- = %i\n", y);

    // Augmented assignment operatores
    // x+=a, x = x + a  increments a variable by a
    // x-=a, x = x - a  decrements a variable by a
    // x*=a, x = x * a  multiplies a variable by a
    // x/=a, x = x / a  divides itself
    // x%=a, x = x % a  modulus by a and sets it to itself

    // User input
    // ints
    int age;
    printf("How old are you? :");
    scanf("%i", &age);
    printf("You are %i\n", age);

    char name[25]; // set bytes, if max, it overflows
    printf("What's your name? "); // ignores white space, so Vercil Juan just becomes Vercil
    scanf("%s", &name);
    printf("Hello, %s\n", name);

    printf("What's your name? ");
    fgets(name, 25, stdin); // includes whitespace
    name[strlen(name)-1] = '\0';
    
    printf("Hello, %s", name);
    return 0;
}
