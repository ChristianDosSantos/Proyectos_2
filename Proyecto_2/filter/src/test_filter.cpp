#include <iostream>
#include <fstream>
using namespace std;

extern "C"{
	#include "filter.h"
}

//Variables for filter
filter fil; //Instance       
unsigned char f_P=10; 			 
int f_b[11]={2,3,7,12,17,18,17,12,7,3,2};  
int f_input[10]={0};  



int main(int argc, char * argv[]){

	int n=stoi(argv[1]); // sim time
	int input=10000; //input value

	init_filter(&fil,f_P,f_b,f_input);
	
	//File creation
	ofstream file;
	file.open("test/filter.dat", ios::out | ios::trunc);

	for (int i = 0; i < n; i++){
		file << eval_filter(&fil,input);
		if(i<n-1)
			file << ",";
	}
	


	return 0;
}
