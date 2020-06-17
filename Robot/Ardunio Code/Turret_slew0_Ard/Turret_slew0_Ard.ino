/*
  http://helloraspberrypi.blogspot.com/2014/12/raspberry-pi-send-block-of-data-to.html
*/
 
// Include the Wire library for I2C
#include <Wire.h>
 
#define LED_PIN 13
boolean ledon = HIGH;
byte slave_address = 7;
int echonum = 0;    // added

void setup() {
//  // set up the LCD's number of columns and rows:
//  lcd.begin(16, 2);
//  // Serial.print startup message to the LCD.
//  lcd.Serial.print("Arduino Uno");
//  
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);
//  
  Serial.begin(9600);      // open the serial port at 9600 bps: 
  Serial.print("Arduino Nano");
  Serial.print('\n');
  Wire.begin(slave_address);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);   // added
}

void loop() {

}

void requestEvent(){    // added

  Wire.write(echonum);  // added
  toggleLED();          // added
}
void receiveEvent(int howMany) {
//  lcd.clear();
  
  int numOfBytes = Wire.available();
  //display number of bytes and cmd received, as bytes
//  lcd.setCursor(0, 0);
//  lcd.print("len:");
//  lcd.print(numOfBytes);
//  lcd.print(" ");
// 
  Serial.print("len:");
  Serial.print(numOfBytes);
  Serial.print(" "); 
  Serial.print('\n');
  byte b = Wire.read();  //cmd
//  lcd.print("cmd:");
//  lcd.print(b);
//  lcd.print(" ");
  Serial.print("cmd:");
  Serial.print(b);
  Serial.print(" ");
  Serial.print('\n');

  //display message received, as char
//  lcd.setCursor(0, 1);
  for(int i=0; i<numOfBytes-1; i++){
    char data = Wire.read();
//    lcd.print(data);
    Serial.print(data);
  }
  
  toggleLED();
  echonum = numOfBytes-1;   // added

}

void toggleLED(){
  ledon = !ledon;
  if(ledon){
    digitalWrite(LED_PIN, HIGH);
  }else{
    digitalWrite(LED_PIN, LOW);
  }
}
