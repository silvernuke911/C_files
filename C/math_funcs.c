# include <math.h>
# include <stdio.h>

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

int main(){
    math_funcs();
    double circ = circ_circumference();
    printf("%f\n",circ);
    double hypot = hypotenuse();
    printf("%f\n",hypot);

    int legal;
    legal = legal_age();
    if (legal == 1){
        printf("You may enter");
    } else {
        printf("You shouldn't be here");
    }
    return 0; 
}