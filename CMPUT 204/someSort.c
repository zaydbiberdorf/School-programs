// some sort CMPUT204 - Zayd Biberdorf
#include <stdio.h>
#include <math.h>
void someSort(int A[], int n, int b, int e){
    int temp;
    if(e == (b+1)){
        if(A[b] > A[e]){
            temp = A[b];
            A[b] = A[e];
            A[e] = temp;
        }
    }else if(e > (b+1)){
        int p = floor((e - b + 1)/3);
        someSort(A, 9, b, e-p);
        someSort(A, 9, b+p, e);
        someSort(A, 9, b, e-p);
        
    }
}

int main(){
    int A[] = {8, 1, 4, 9, 7, 3, 2, 6, 5};
    someSort(A, 9, 0, 8);
    for(int i = 0; i < 9; i++){
        printf("%d, ", A[i]);
    }
    printf("\n");
}