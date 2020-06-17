/*
 * Routine to receive a command from the RPi and slew the camera turret
 * 
 * 20200519;1832 It is not clean, but it does work.  Using Turret_slew)_RPi to send the angle command, the servo will slew to that angle.
*/

#include <Servo.h>
#include <Wire.h>

#define LED_PIN 13
boolean ledon = HIGH;
char data;
Servo cameraservo;  // create servo object to control a servo

int pos = 90;    // variable to store the servo position
String angle;
byte slave_address = 7;
int echonum = 0;    // added
 
void setup() {
    cameraservo.attach(9);  // attaches the servo on pin 9 to the servo object
    cameraservo.write(pos); // slew to nominal (zero) position with will align forward on center axis of robot

  Wire.begin(slave_address);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);   // added

// this section to be replaced with receipt of angle from RPi over i2c    
    Serial.begin(9600); 
    delay(2000); 
    Serial.println("Enter degrees:");
}
void toggleLED(){
  ledon = !ledon;
  if(ledon){
    digitalWrite(LED_PIN, HIGH);
  }else{
    digitalWrite(LED_PIN, LOW);
  }
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
angle = ' ';
  for(int i=0; i<numOfBytes-1; i++){
    char data = Wire.read();
//    lcd.print(data);
    Serial.print('\n');
    Serial.print(data);
    Serial.print('\n');
    angle.concat(data);
//    angle = data;
    Serial.print(angle);
  }
  
  toggleLED();
  echonum = numOfBytes-1;   // added

}

 
 
void loop() {
//    if(Serial.available()){
//        angle = Serial.readStringUntil('\n');
//        int pos = angle.toInt();
//        cameraservo.write(pos); // slew to input angle
//        delay (500);    // wait 1/2 second
//
//        String a = String(pos);
// 
//        Serial.println("Degrees is: " + a + "!");
//    }
int pos = angle.toInt();
cameraservo.write(pos); // slew to input angle
delay (500);    // wait 1/2 second

String a = String(pos);

Serial.println("Degrees is: " + a + "!");

}
