#include "config.h"
#ifdef MRAA_LIBRARY

#include <stdint.h>
#include <stdio.h>
#include "native_wuclasses.h"
#include "LCD_RGB_Suli.h"

void wuclass_grove_lcd_setup(wuobject_t *wuobject) {
	rgb_lcd_init(6);
	rgb_lcd_clear();
	rgb_lcd_setRGB(255,0,0);
}

void wuclass_grove_lcd_update(wuobject_t *wuobject) {
	int16_t value;
    wkpf_internal_read_property_int16(wuobject, WKPF_PROPERTY_GROVE_LCD_VALUE, &value);

    char buffer[128];
    snprintf(buffer, 128, "Value: %d", value);
    rgb_lcd_setCursor(0, 0);
    rgb_lcd_print(buffer);
}
#endif