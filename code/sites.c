#include <stdio.h>
#include <string.h>

void score(const char* dna, double p[], int n, double result[]) {
    int i,j,k,N;
    double r; 
    N = strlen(dna)-n+1;
    for (i=0; i<N; i++){
        r = 0;
        for (j=0; j<n; j++){
            switch(dna[i+j]) {
                case 'a': { k=0; break; }
                case 'c': { k=1; break; }
                case 'g': { k=2; break; }
                case 't': { k=3; break; }
            }
            r += p[j*4 + k];
        }
        result[i] = r;
    }
}