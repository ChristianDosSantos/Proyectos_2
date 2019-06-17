/*
 * functions.c0
 *
 *  Created on: Feb 13, 2017
 *      Author: JesúsC
 */
/* Including needed modules to compile this module/procedure */
#include "Cpu.h"
#include "Events.h"
#include "AS1.h"
/* Include shared modules, which are used for whole project */
#include "PE_Types.h"
#include "PE_Error.h"
#include "PE_Const.h"
#include "IO_Map.h"
#include "functions.h"

void send_byte(char data){
	
	while(AS1_SendChar(data) != ERR_OK){}
	
}

void make_packet(unsigned short analogCh1,unsigned short analogCh2,bool digitalCh1,bool digitalCh2,unsigned long* data){
	
	*data=  0x00808080;
	*data|= 0x003F & analogCh2;
	*data|= (0x0FC0 & analogCh2) << 2;
	*data|= (0x0000003F & (unsigned long) analogCh1) << 16;
	*data|= (0x00000FC0 & (unsigned long) analogCh1) << 18;
	if(digitalCh1)
		*data|= 0x00004000;
	if(digitalCh2)
		*data|= 0x00000040;
		
}



