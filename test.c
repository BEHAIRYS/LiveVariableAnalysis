#include <stdio.h>

int main(){
	int x,z;
	scanf("%d", &z);
	x = 4;
	x = x + z;
	if(z > 3){
		z--;
	}
	x = x + z;
	return 0;
}
