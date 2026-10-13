/*
 * hsv2rgb.c
 *
 *  Created on: Jul 13, 2026
 *      Author: Aaron
 */

#include "hsv2rgb.h"

RGB_color_t encoder2rgb(uint8_t encoder_value) {
	RGB_color_t color;

	uint32_t hue =(uint32_t)encoder_value * 6;

	uint8_t sector = hue / 256;
	uint8_t value = hue % 256;

    switch(sector) {
        case 0: color.r = 255;       color.g = value;     color.b = 0;         break; // Rot zu Gelb
        case 1: color.r = 255-value; color.g = 255;       color.b = 0;         break; // Gelb zu Grün
        case 2: color.r = 0;         color.g = 255;       color.b = value;     break; // Grün zu Cyan
        case 3: color.r = 0;         color.g = 255-value; color.b = 255;       break; // Cyan zu Blau
        case 4: color.r = value;     color.g = 0;         color.b = 255;       break; // Blau zu Magenta
        case 5: color.r = 255;       color.g = 0;         color.b = 255-value; break; // Magenta zu Rot
    }

    /*TIMx->CCR1 = 255 - r; // Rot
    TIMy->CCR2 = 255 - g; // Grün
    TIMz->CCR3 = 255 - b; // Blau*/

    return color;
}
