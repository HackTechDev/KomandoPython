#include <stdio.h>

#include "h-define.h"
#include "h-type.h"
#include "defines.h"
#include "externs.h"

int main(int argc, char** argv)
{
	int x, y;
	
	srand(time(NULL));

	generate_cave();


	vectorize();

	return 0;
}
