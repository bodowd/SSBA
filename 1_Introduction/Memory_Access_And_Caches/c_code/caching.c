#include <stdio.h>
#include <time.h>

#define ITERS 1000000000

void printSpeed(void (*f)());
void v2();
void v1();

int main(int argc, char **argv) {
  printSpeed(v2);
  printSpeed(v1);
}

void v2() {
  long sum1 = 0;
  for (long i = 0; i < ITERS; i++) {
    sum1 += i;
  };
  long sum2 = 0;
  for (long i = 0; i < ITERS; i++) {
    sum2 += i;
  };
}

void v1() {
  long sum1 = 0;
  long sum2 = 0;
  for (long i = 0; i < ITERS; i++) {
    sum1 += i;
    sum2 += i;
  };
}

void printSpeed(void (*f)()) {
  clock_t start = clock();
  f();
  float secs = (float)(clock() - start) / CLOCKS_PER_SEC;
  float ops = ITERS / secs;
  printf("Clock speed approx %.3f GHz\n", ops / (float)(ITERS));
}
