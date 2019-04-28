#include <iostream>
using namespace std;

extern "C"{
	#include "filter.h"
}


int main(){

	cout << "Hello world\n";
	return filter(5);

	}
