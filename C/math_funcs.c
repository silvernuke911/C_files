# include <math.h>
# include <stdio.h>
# include <time.h>
# include <stdbool.h> 
# include <string.h>

int math_funcs(){
    double A = sqrt(10);
    double B = pow(2,32);
    double C = 3.14145;
    int D = round(C);
    int E = ceil(C);
    int F = floor(C);
    double G = fabs(-C);
    double H = log(C);
    double I = sin(45);
    double J = cos(45);
    double K = tan(45);
    printf("%.15f\n", A);
    printf("%f\n", B);
    printf("%i\n", D);
    printf("%i\n", E);
    printf("%i\n", F);
    printf("%f\n", G);
    printf("%f\n", H);
    printf("%f\n", I);
    printf("%f\n", J);
    printf("%f\n", K);
    return 0;
}


float circ_circumference(){
    const double pi = 3.141592654;
    double radius;
    double circum;
    double area;

    printf("Enter the value of r: ");
    scanf("%lf", &radius);

    circum = 2*pi*radius;
    area = pi * radius * radius;
    return circum;
}

// If else shit
int legal_age(){
    int age;
    printf("Enter your age: ");
    scanf("%i", &age);
    if (age >= 18){
        return 1;
    }
    return 0;
}

// logical operators
int log_op(){
    // && is the logical and operator
    // || is the or logical operator
    // ! is the not logical operator
}
float hypotenuse(){
    double x;
    double y;
    double hypot;

    printf("Enter the value of x : ");
    scanf("%lf", &x);
    printf("Enter the value of y : ");
    scanf("%lf", &y);

    hypot = sqrt(x*x + y*y);

    return hypot;
}

// switch cases
int switcher() {
    char grade;
    printf("Enter a letter grade: ");
    scanf(" %c", &grade);  // Added space before %c to ignore newline

    switch (grade) {
        case 'A':
            printf("Outstanding\n");
            break;
        case 'B':
            printf("Exemplary\n");
            break;
        case 'C':
            printf("Ehh\n");
            break;
        case 'D':
            printf("Lol bro fr\n");
            break;
        case 'F':
            printf("You failed\n");
            break;
        default:
            printf("Put a valid letter, idiot\n");
            break;
    }
    return 0;
}

void birthday(char name[], int age){
    printf("Happy birthday to you, happy birthday to you\n");
    printf("Happy birthday to you, happy birthday dear %s\n", name);
    printf("You are now %i years old!\n", age);
}

int forlooper(){
    int numbers[] = {10, 20, 30, 40, 50};
    int size = sizeof(numbers) / sizeof(numbers[0]);

    for (int i = 0; i < size; i++) {
        printf("Element %d: %d\n", i, numbers[i]);
    }
    return 0;
}


float temp_convert(){
    char unit;
    float temp;

    printf("\nIs the temperature in F or C?: ");
    scanf(" %c", &unit);  // 

    printf("\nWhat is the temperature value?: ");
    scanf("%f", &temp);   //

    float temp_c;
    char unit_c;

    if (unit == 'C' || unit == 'c') {
        unit_c = 'F';
        temp_c = (9.0 / 5.0) * temp + 32;  
    } else if (unit == 'F' || unit == 'f') {
        unit_c = 'C';
        temp_c = (temp - 32) * (5.0 / 9.0);  
    } else {
        printf("Invalid unit entered.\n");
        return 0;
    }

    printf("The converted temperature is %.2f degrees %c\n", temp_c, unit_c);
    return temp_c;
}
// Function calls
double square(double x){
    return x*x;
}
// Ternary operators
int find_max(int x, int y){
    // short cut for if else
    // (condition) ? value if true: value if false
    return (x > y) ? x : y;
}
// Function prototypes
// function declearation w/o body, before main()
// Ensures that calls to a function are made with the correct arguments
// Place before main
void hello(char[], int);
    // function prototype that ensures that the arguments are correct. 
    // If there are functions after maim

//string functions
int stringer(){
    char string1[] = "Heil";
    char string2[] = "Hitler";

    strlwr(string1);                // converts the entire string to lowercase
    strupr(string1);                // converts the entire string to uppercase
    strcat(string1, string2);       // concatenates the strings
    strncat(string1, string2, 1);   // appends n characters from string2 to stirng 1
    strcpy(string1, string2);       // copy string2 to string1, deletes the contents of str1
    strncpy(string1, string2, 4);   // copy the first n characters from string2 to string1
    strset(string1, '?');           // sets all the characters of a string to a given character
    strnset(string1, 'x', 1);       // sets the first n characters of a string to a given character
    strrev(string1);                // reverses a string
    strlen(string1);                // returns the length of a string
    strcmp(string1, string2);       //string compare all characters
    strncmp(string1, string2, 1);   // string compare the first n characters
    strcmpi(string1, string2);      // string compare all (ignore case)
    strnicmp(string1, string2, 1);  // string compare the first n characters (ignore case)
}
// For loop
int forlooper2(){
    // for( initialization ; end condition ; increment)
    for(int i = 1 ; i <= 10 ; i++){
        printf("%i\n", i);
    }
    for(int i = 0 ; i <= 10 ; i+=2){
        printf("%i\n", i);
    }
    for(int i = 10 ; i >= 1 ; i--){
        printf("%i\n", i);
    }
    return 0;
}
// While loop - executes while a condition is true, will not execute if condition was false in the first place
int whilelooper(){
    char name[25];
    printf("What is your name? : ");
    fgets(name, 25, stdin);
    name[strlen(name)-1] = '\0';

    while (strlen(name)==0){
        printf("Please enter your name again\n");
        printf("What is your name? : ");
        fgets(name, 25, stdin);
        name[strlen(name)-1] = '\0';
    }

    printf("Hello %s", name);
    return 0;
}

// do while loop - always executes a piece of code once, and then check  if the conditon is still true
int dowhiler(){
    int number = 0;
    int sum = 0;
    do{
        printf("Enter a number gtr than 0 : ");
        scanf("%d", &number);
        if (number > 0){
            sum += number;
        }
    } while (number > 0);
    printf("%i", sum);
    return 0;
}
// nested loops ; for loops within loops
int nester(){
    int rows;
    int cols;
    char symb;

    printf("Enter number of rows: ");
    scanf("%i", &rows);
    printf("Enter number of columns: ");
    scanf("%i", &cols);
    printf("Enter a symbol to use: ");
    scanf(" %c", &symb);

    for (int i = 1; i <= rows; i++){
        for (int j = 1; j <= cols; j++){
            printf("%c", symb);
        }
        printf("\n"); // Newline after each row
    }
    return 0;
}
// Difference of continue and break
    // contiue - skips the rest of the code and returns back to the start
    // break   - exits the loop
 
int main(){
    // math_funcs();
    // double circ = circ_circumference();
    // printf("%f\n",circ);
    // double hypot = hypotenuse();
    // printf("%f\n",hypot);

    // int legal;
    // legal = legal_age();
    // if (legal == 1){
    //     printf("You may enter\n");
    // } else {
    //     printf("You shouldn't be here\n");
    // }
    //

    //switcher();
    //forlooper();

    // // temp_convert();
    // char name[] = "Vers";
    // int age = 22;
    // birthday(name, age);
    // double a = 1.50;
    // double x = square(a);
    // printf("%.15lf", x);
    // int max = find_max(5,6);
    // printf("%i", max);
    // forlooper2();
    // whilelooper();
    //dowhiler();
    nester();
    return 0; 
}