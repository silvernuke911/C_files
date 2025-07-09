#include <stdio.h>
#include <math.h>
#include <string.h>

#define freezing_pt 32.0f 
#define scale_factor (5.0f/9.0f)

float converter(float value, char *mode){
    float result;
    if (strcmp(mode, "C2F") == 0) {
        result = (value / scale_factor) + freezing_pt;
    }
    else if (strcmp(mode, "F2C") == 0) {
        result = (value - freezing_pt) * scale_factor;
    } else {
        printf("Error: Invalid mode\n");
        return NAN;
    }
    return result;
}

int convert_scan() {
    printf("=================================\n");
    printf("         TEMP CONVERTER          \n");
    printf("---------------------------------\n");
    char mode[3];
    float value;
    printf("Mode (C2F or F2C): ");
    scanf("%s", &mode);
    printf("Value            : ");
    scanf("%f", &value);
    float result = converter(value, mode);
    if (isnan(result)) {
        printf("Invalid mode. Try again\n");
        return 0;
    }
    printf("=================================\n");
    printf("Result : %.3f", result);
    return 0;
}
int main(){
    convert_scan();
    return 0;
}