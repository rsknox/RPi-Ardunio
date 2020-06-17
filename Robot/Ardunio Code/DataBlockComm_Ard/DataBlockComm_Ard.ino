/*
 * from http://bradsduino.blogspot.com/2013/03/sending-data-from-arduino-to-raspberry.html
 * Collects data from sensors attached to Ardunio and sends to RPi
 * 20200518: I forced integer values into a byte array and did a Wire.write of that array, and it did get transmitted to the RPi
 *    I think if I want to send character data, I have to do an 'ord' coversion, or maybe char(x)
 * 
 * 
 */

#include <Wire.h>

//#include <OneWire.h>

const int DEV_CNT = 4, I2C_ADDR = 0x03;


byte datab[12] = {40,50,60,70,80,90,100,110,120,130,140,150};
char datac[12] = {'a', 'r', 'd', 'u', 'i', 'n', 'o', ' ', 'N','A', 'N', 'O'};

//OneWire ds(10);  // 1wire bus on pin 10
int j = 0;
float fahrenheit[DEV_CNT];  //RK; looks like a 4 element array
byte dev[DEV_CNT][8];   //RK; this must be a 4x8 array  (32 bytes)

void setup(void) {
  Wire.begin(I2C_ADDR);
  Wire.onRequest(requestEvent); //Register i2c request handler 
}

void loop(void) {
  byte i, present = 0, type_s = 0, data[12], addr[8];
//  if(!ds.search(addr)) {
//    ds.reset_search();
//    delay(250);
//    return;
//  } 
  // Read 8-byte device ID
//  load some test data
  data[0] = 30;
  data[1] = 40;
  data[2] = 50;
  data[3] = 60;
  data[4] = 70;
  data[5] = 80;
  data[6] = 90;
  data[7] = 100;
  data[8] = 110;
  data[9] = 120;
  data[10] = 130;
  data[11] = 140;
//  addr[8] = {201, 202, 203, 204, 205, 206, 207, 208};  //RK; load some test data
  addr[0] = 201;
  addr[1] = 202;
  addr[2] = 203;
  addr[3] = 204;
  addr[4] = 205;
  addr[5] = 206;
  addr[6] = 207;
  addr[7] = 208;
  for( i = 0; i < 8; i++) { dev[j][i] = addr[i]; }
//  ds.reset();
//  ds.select(addr);
//  ds.write(0x44,1);   // start conversion, parasite power on   
//  delay(750);      
//  present = ds.reset();
//  ds.select(addr);    
//  ds.write(0xBE);     // Read Scratchpad

//  for ( i = 0; i < 9; i++) {  data[i] = ds.read(); }
  for ( i = 0; i < 9; i++) {  data[i] = data[i]; }
  // convert the data to actual temperature
  unsigned int raw = (data[1] << 8) | data[0];
  fahrenheit[j] = (float) raw / 16.0 * 1.8 + 32.0;
  ++j %= DEV_CNT;  // Increment j but keep within range of device count
}

void requestEvent() // Handle i2c requests
{
  // Buffer to hold temp data, 6 bytes for each device
  byte buffer[DEV_CNT*4];
  // Populate buffer with temp. data
  for(int a = 0; a < DEV_CNT; a++) {
    byte* b = (byte*) &fahrenheit[a];
    // 4 bytes for each float
    for(int i = 0; i < 4; i++) {
      buffer[a*DEV_CNT+i] = b[i];
    }
  }
  // Send data over i2c connection
//  Wire.write(buffer, DEV_CNT*4);
//  Wire.write(datab, 12); 
  Wire.write(datac, 12);  
}
