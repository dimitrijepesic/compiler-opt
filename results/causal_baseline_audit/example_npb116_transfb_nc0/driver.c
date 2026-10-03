
// Fixed-vector behaviour check for transfb_nc0 (not a proof of equivalence).
// r_init and qbnew are external to the extracted function in the original
// module as well; their definitions here are written for this test only.
#include <stdio.h>
#include <string.h>
double qbnew[2][5][3];
void r_init(double *a, int n, double v) { for (int i = 0; i < n; ++i) a[i] = v; }
void transfb_nc0(double *tmor, double *tx);
int main(void) {
  double tmor[25], tx[25];
  unsigned long long s = 88172645463325252ULL;
  for (int round = 0; round < 4; ++round) {
    for (int i = 0; i < 25; ++i) { s ^= s << 13; s ^= s >> 7; s ^= s << 17; tmor[i] = (double)(s % 2000003) / 977.0 - 1000.0; }
    for (int i = 0; i < 25; ++i) { s ^= s << 13; s ^= s >> 7; s ^= s << 17; tx[i] = (double)(s % 1000003) / 313.0 - 1500.0; }
    for (int i = 0; i < 30; ++i) { s ^= s << 13; s ^= s >> 7; s ^= s << 17; ((double *)qbnew)[i] = (double)(s % 500009) / 127.0 - 2000.0; }
    transfb_nc0(tmor, tx);
    for (int i = 0; i < 25; ++i) { unsigned long long b; memcpy(&b, &tmor[i], 8); printf("%d %d %016llx\n", round, i, b); }
  }
  return 0;
}
