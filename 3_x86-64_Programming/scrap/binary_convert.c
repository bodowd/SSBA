#include <math.h>
#include <stdio.h>
#include <string.h>

int binary_convert(char s[]);

int binary_convert(char s[]) {
  int i = 0;
  int place = strlen(s) - 1;
  int total = 0;
  while (s[i] != '\0') {
    if (s[i] == '1') {
      // total += (int)pow(2, place);
      // calculate pow(2, place) with bit shift
      total += 1 << place;
    }
    place -= 1;
    i++;
  }
  return total;
}

int main() {
  char s[20] = "111111";
  printf("%d\n", binary_convert(s));
  return 0;
}
