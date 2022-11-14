// ---------------------------------------------------------------- 
//                                                                  
// DS18B20 Temperature Sensor on an ESP32
//
// (c) Rolf Wuthrich, 
//     2022 Concordia University
//
// author:  Rolf Wuthrich
// email:   rolf.wuthrich@concordia.ca
//
// This software is copyright under the BSD license
//
// --------------------------------------------------------------- 

// Demonstrates how to setup an MTConnect Adapter which
// reads the temperaure from a DS18B20 Temperature Sensor
//
// The adapter sends SHDR format on the serial port
// The adapter assumes the following configuration 
// in the MTConnect device model:
//
//   <DataItem category="SAMPLE" id="Temp" type="TEMPERATURE" units="CELCIUS"/>
//
//
// Required libraries :
// (all availables via Sketch > Include Library > Manage Libraries)
//
// - OneWire library by Paul Stoffregen
//   https://github.com/PaulStoffregen/OneWire
//   https://www.pjrc.com/teensy/td_libs_OneWire.html
//
// - DallasTemperature library by Miles Burton
//   https://github.com/milesburton/Arduino-Temperature-Control-Library


#include <OneWire.h>
#include <DallasTemperature.h>

// GPIO where the DS18B20 is connected to
const int oneWireBus = 4;     

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(oneWireBus);

// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);

// Global temperature variable
float tempOld;


void sendSHDR(float temp)
{
  Serial.print("|Temp|");
  Serial.println(temp);
}

void setup() {
  // Start the Serial Monitor
  Serial.begin(115200);
  // Start the DS18B20 sensor
  sensors.begin();
  tempOld = 0.0;
}

void loop() {
  
  sensors.requestTemperatures(); 
  float temp = sensors.getTempCByIndex(0);
  if (temp!=tempOld) {
    sendSHDR(temp);
  }
  tempOld = temp;
 
  delay(100);
}
