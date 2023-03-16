#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define GIGA 1000000000
#define ITERS 4000

void v2();
void v1();
void printSpeed(void (*f)());

int main() {
  printSpeed(v1);
  printSpeed(v2);
}

void v1() {
  printf("v1\n");
  int i, j;
  static int x[ITERS][ITERS];
  for (i = 0; i < ITERS; i++) {
    for (j = 0; j < ITERS; j++) {
      x[j][i] = i + j;
    }
  }
}

void v2() {
  printf("v2\n");
  int i, j;
  static int x[ITERS][ITERS];
  for (j = 0; j < ITERS; j++) {
    for (i = 0; i < ITERS; i++) {
      x[j][i] = i + j;
    }
  }
}

void printSpeed(void (*f)()) {
  clock_t start = clock();
  f();
  float secs = (float)(clock() - start) / CLOCKS_PER_SEC;
  // float ops = ITERS / secs;
  // printf("Clock speed approx %.3f GHz\n", ops / (float)(GIGA));
  printf("Time elapsed: %.3f\n", secs);
}

// We imagine 2D array like this
// 0,0 | 0,1 | 0,2 | 0,3
// ----+-----+-----+----
// 1,0 | 1,1 | 1,2 | 1,3
// ----+-----+-----+----
// 2,0 | 2,1 | 2,2 | 2,3

// in memory it is a 1d array
// 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10  | 11
// 0,0 | 0,1 | 0,2 | 0,3 | 1,0 | 1,1 | 1,2 | 1,3 | 2,0 | 2,1 | 2,2 | 2,3

// in v1, we loop over the second element first, so we access
// x[0][0], x[1][0], x[2][0],... then x[0][1], x[1][1], x[2][1]
// this gets index 0, then index 4, then index 8
// these are non sequential, so when the computer loads cache lines -- bringing
// data from memory to CPU in little chunks -- so each time it brings something
// from memory, it can only operate on a small part of it. Not efficient.
// bring lots of data to the cache, but most is not used. So each time you have
// to go to the memory

// in v2, we loop over first item first:
// x[0][0], x[0][1], x[0][2],.. x[1][0], x[1][1], x[1][2]
// this gets index 0,1,2,3,4,...n.
// this is in sequential order and the cache will have more hits
