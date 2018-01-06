#include "debug.h"
#include "native_wuclasses.h"
#include <avr/io.h>
#include <stdlib.h>

void wuclass_slider_setup(wuobject_t *wuobject) {}

void wuclass_slider_update(wuobject_t *wuobject) {
  // Pieced together from IntelDemoLightSensorV1.java, Adc.java and native_avr.c

  // Adc.setPrescaler(Adc.DIV64);
  ADCSRA = _BV(ADEN) | (6 & 7);  // set prescaler value

  // Adc.setReference(Adc.INTERNAL);
  ADMUX = (3 << 6) & 0xc0;              // set reference value

  // light_sensor_reading = Adc.getByte(Adc.CHANNEL0);
  // ADLAR = 1
  uint8_t channel = 2; // NOTE: Adc.CHANNEL0 means a value of 0 for the channel variable, but other ADC channels don't map 1-1. For instance channel 15 is selected by setting the channel variable to 39. See below for a list.
  ADMUX = (ADMUX & 0xc0) | _BV(ADLAR) | (channel & 0x0f);
  ADCSRB |= (channel & 0x20)>>2;

  // do conversion
  ADCSRA |= _BV(ADSC);                  // Start conversion
  while(!(ADCSRA & _BV(ADIF)));         // wait for conversion complete
  ADCSRA |= _BV(ADIF);                  // clear ADCIF

  // After this:
  // 0 <= ADCH <= 255
  // We want to recalibrate this to the range between the low and high values for the slider
  int16_t low;
  int16_t high;
  wkpf_internal_read_property_int16(wuobject, WKPF_PROPERTY_SLIDER_LOW_VALUE, &low);
  wkpf_internal_read_property_int16(wuobject, WKPF_PROPERTY_SLIDER_HIGH_VALUE, &high);
  int16_t range = high-low;
  int16_t last_output;
  wkpf_internal_read_property_int16(wuobject, WKPF_PROPERTY_SLIDER_OUTPUT, &last_output);
  DEBUG_LOG(DBG_WKPFUPDATE, "WKPFUPDATE(Slider): Sensed last_output is %d\n", last_output);
  int16_t this_output = (int16_t)((int32_t)ADCH*range/255+low);
  DEBUG_LOG(DBG_WKPFUPDATE, "WKPFUPDATE(Slider): Sensed this_output is %d\n", this_output);
  if(abs(this_output - last_output) <= 5)
  {
    wkpf_internal_write_property_int16(wuobject, WKPF_PROPERTY_SLIDER_OUTPUT, last_output);
    DEBUG_LOG(DBG_WKPFUPDATE, "WKPFUPDATE(Slider): Sensed %d, low %d, high %d, last_output %d\n", ADCH, low, high, last_output);
  }else{ 
    wkpf_internal_write_property_int16(wuobject, WKPF_PROPERTY_SLIDER_OUTPUT, this_output);
    DEBUG_LOG(DBG_WKPFUPDATE, "WKPFUPDATE(Slider): Sensed %d, low %d, high %d, this_output %d\n", ADCH, low, high, this_output);
  }
}

// ADC CHANNEL 0,  value for channel variable: 0
// ADC CHANNEL 1,  value for channel variable: 1
// ADC CHANNEL 2,  value for channel variable: 2
// ADC CHANNEL 3,  value for channel variable: 3
// ADC CHANNEL 4,  value for channel variable: 4
// ADC CHANNEL 5,  value for channel variable: 5
// ADC CHANNEL 6,  value for channel variable: 6
// ADC CHANNEL 7,  value for channel variable: 7
// ADC CHANNEL 8,  value for channel variable: 32
// ADC CHANNEL 9,  value for channel variable: 33
// ADC CHANNEL 10, value for channel variable: 34
// ADC CHANNEL 11, value for channel variable: 35
// ADC CHANNEL 12, value for channel variable: 36
// ADC CHANNEL 13, value for channel variable: 37
// ADC CHANNEL 14, value for channel variable: 38
// ADC CHANNEL 15, value for channel variable: 39
