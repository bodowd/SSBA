#include <math.h>
#include <stdio.h>
#include <string.h>

int binary_convert(char s[]);

int binary_convert(char s[]) {
  int i;
  int place = 0;
  int total = 0;
  for (i = 0; i < strlen(s); i++) {
    char s1 = s[i];
    if (strcmp(&s1, "1")) {
      // total += (int)pow(2, place);
      // calculate pow(2, place) with bit shift
      total += 1 << place;
    }
    place += 1;
  }
  return total;
}

int main() {
  char s[20] = "1110";
  printf("%d\n", binary_convert(s));
  return 0;
}
