# include <math.h>
# include <stdio.h>
# include <time.h>
# include <stdlib.h>

int main(){
    int N = 100;
    for (int i = 1 ; i<=N; i++ ){
        if (i%5==0 && i%3==0){
            printf("Fizzbuz\n");
        } else if (i%3==0){
            printf("Fizz\n");
        } else if (i%5==0){
            printf("Buzz\n");
        } else {
            printf("%i\n", i);
        }
    }
    printf("Press Enter to exit...");
    getchar();  // Waits for a key press
    return 0;
}