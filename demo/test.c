/* #include <stdio.h>  <-- OVO PRAVI PROBLEM, BRISEMO GA */

/* Rucno kazemo C-u da printf postoji, da ne trazi stdio.h */
int printf(const char *format, ...);

int factorial(int n) {
    int i;
    int res = 1;
    int temp = 0;
    
    /* Bespotrebna petlja za optimizaciju */
    for(int k=0; k<100; k++) {
        temp += k;
    }
    
    if (n <= 1) return 1;
    
    for (i = 1; i <= n; i++) {
        res = res * i;
    }
    return res;
}

int main() {
    int number = 10;
    int result = factorial(number);
    
    printf("Faktorijel broja %d je: %d\n", number, result);
    return 0;
}