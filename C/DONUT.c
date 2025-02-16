#include <stdio.h>
#include <math.h>
#include <string.h>
#include <unistd.h>  // For usleep

#define PI 3.1415926535
#define SCREEN_WIDTH 80
#define SCREEN_HEIGHT 24
#define R1 1.0   // Inner radius of torus
#define R2 2.0   // Outer radius of torus
#define K2 5.0   // Distance from viewer to screen
#define K1 15.0  // Scaling factor

void render_frame(double A, double B) {
    char output[SCREEN_WIDTH * SCREEN_HEIGHT];
    double zbuffer[SCREEN_WIDTH * SCREEN_HEIGHT];
    memset(output, ' ', sizeof(output));
    memset(zbuffer, 0, sizeof(zbuffer));

    for (double theta = 0; theta < 2 * PI; theta += 0.07) {
        for (double phi = 0; phi < 2 * PI; phi += 0.02) {
            double costheta = cos(theta), sintheta = sin(theta);
            double cosphi = cos(phi), sinphi = sin(phi);

            double circlex = R2 + R1 * costheta;
            double circley = R1 * sintheta;

            double x = circlex * cos(B) - circley * sin(B);
            double y = circlex * sin(A) * sin(B) + circley * cos(A) + sinphi * cos(B);
            double z = K2 + circlex * cos(A) * sin(B) - circley * sin(A);
            double ooz = 1 / z;

            int xp = (int)(SCREEN_WIDTH / 2 + K1 * x * ooz);
            int yp = (int)(SCREEN_HEIGHT / 2 - K1 * y * ooz);
            int idx = xp + yp * SCREEN_WIDTH;

            if (idx >= 0 && idx < SCREEN_WIDTH * SCREEN_HEIGHT) {
                if (ooz > zbuffer[idx]) {
                    zbuffer[idx] = ooz;
                    double luminance = cosphi * costheta * sin(B) - sinphi * sintheta * cos(A) + cosphi * sintheta * sin(A) + sinphi * cos(A);
                    int luminance_index = (int)(luminance * 8);
                    const char *chars = ".,-~:;=!*#$@";
                    output[idx] = chars[luminance_index > 0 ? luminance_index : 0];
                }
            }
        }
    }

    printf("\x1b[H");
    for (int i = 0; i < SCREEN_WIDTH * SCREEN_HEIGHT; i++) {
        putchar(i % SCREEN_WIDTH ? output[i] : '\n');
    }
}

int main() {
    double A = 0, B = 0;
    while (1) {
        render_frame(A, B);
        A += 0.04;
        B += 0.02;
        usleep(50000);
    }
    return 0;
}