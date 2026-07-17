/*
 * hsv2rgb.h
 *
 *  Created on: Jul 13, 2026
 *      Author: Aaron
 */

#ifndef HSV2RGB_H_
#define HSV2RGB_H_

#include "main.h"
//#include "stdint.h"

typedef struct {
	uint8_t r;
	uint8_t g;
	uint8_t b;
} RGB_color_t;

RGB_color_t encoder2rgb(uint8_t encoder_value);

#endif /* HSV2RGB_H_ */
