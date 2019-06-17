/*
 * functions.h
 *
 *  Created on: Feb 13, 2017
 *      Author: JesúsC
 */

#ifndef FUNCTIONS_H_
#define FUNCTIONS_H_

void send_byte(char data);

void make_packet(unsigned short analogCh1,unsigned short analogCh2,bool digitalCh1,bool digitalCh2,unsigned long* data);



#endif /* FUNCTIONS_H_ */
