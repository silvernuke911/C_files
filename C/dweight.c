#include <stdio.h>
#include <math.h>

/* Computes the dimensional weight of box with 
   dimensions length l, width w, height h, and 
   weight wt*/
int d_weight(int l, int w, int h) {
    int volume = l * w * h;
    int weight = (volume + 165) / 166;

    printf("Dimensions       : %dx%dx%d\n",l,w,h);
    printf("Volume (cb.in.)  : %d\n",volume);
    printf("Dim weight (lbs) : %d\n", weight);
    return 0;
}

int scanner(){
    int h,l,w;
    printf("Enter height of box : ");
    scanf("%d", &h);
    printf("Enter width of box  : ");
    scanf("%d", &w);
    printf("Enter length of box : ");
    scanf("%d", &l);
    d_weight(l,w,h);
    return 0;
}
int main(){
    scanner();
    return 0;
}