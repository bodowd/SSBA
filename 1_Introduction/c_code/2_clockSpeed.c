#include <stdint.h>
#include <stdio.h>
#include <time.h>

#define ITERS 1000000000

void sumLoop();
void multLoop();
void divLoop();
void divWithMultLoop();
void printSpeed(void (*f)());

int main(int argc, char **argv) {
  printf("Sum\n");
  printSpeed(sumLoop);
  printf("Multiplication\n");
  printSpeed(multLoop);
  printf("Division\n");
  printSpeed(divLoop);
}

void sumLoop() {
  long sum = 0;
  for (long i = 0; i < ITERS; i++) {
    sum += i;
  };
}

void multLoop() {
  long prod = 0;
  for (long i = 0; i < ITERS; i++) {
    prod *= i;
  }
}

void divLoop() {
  long div = 1;
  for (long i = 1; i < ITERS; i++) {
    div /= i;
  }
}

void printSpeed(void (*f)()) {
  clock_t start = clock();
  f();
  float secs = (float)(clock() - start) / CLOCKS_PER_SEC;
  float ops = ITERS / secs;
  printf("Clock speed approx %.3f GHz\n", ops / (float)(ITERS));
}
