#include <stdio.h>
#include <time.h>

#define ITERS 1000000000

int main(int argc, char **argv) {
  clock_t start = clock();
  for (int i = 0; i < ITERS; i++)
    ;
  float secs = (float)(clock() - start) / CLOCKS_PER_SEC;
  float ops = ITERS / secs;
  printf("Clock speed approx %.3f GHz\n", ops / (float)(ITERS));
}
