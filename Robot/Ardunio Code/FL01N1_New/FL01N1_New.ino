/*
 Copyright (C) 2011 James Coliz, Jr. <maniacbug@ymail.com>
 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 2 as published by the Free Software Foundation.
 */
/**
 * Example: Network topology, and pinging across a tree/mesh network
 *
 * Using this sketch, each node will send a ping to every other node in the network every few seconds. 
 * The RF24Network library will route the message across the mesh to the correct node.
 *
 * This sketch is greatly complicated by the fact that at startup time, each
 * node (including the base) has no clue what nodes are alive.  So,
 * each node builds an array of nodes it has heard about.  The base
 * periodically sends out its whole known list of nodes to everyone.
 *
 * To see the underlying frames being relayed, compile RF24Network with
 * #define SERIAL_DEBUG.
 *
 * Update: The logical node address of each node is set below, and are grouped in twos for demonstration.
 * Number 0 is the master node. Numbers 1-2 represent the 2nd layer in the tree (02,05).
 * Number 3 (012) is the first child of number 1 (02). Number 4 (015) is the first child of number 2.
 * Below that are children 5 (022) and 6 (025), and so on as shown below 
 * The tree below represents the possible network topology with the addresses defined lower down
 *
 *     Addresses/Topology                            Node Numbers  (To simplify address assignment in this demonstration)
 *             00                  - Master Node         ( 0 )
 *           02  05                - 1st Level children ( 1,2 )
 *    32 22 12    15 25 35 45    - 2nd Level children (7,5,3-4,6,8)
 *
 * eg:
 * For node 4 (Address 015) to contact node 1 (address 02), it will send through node 2 (address 05) which relays the payload
 * through the master (00), which sends it through to node 1 (02). This seems complicated, however, node 4 (015) can be a very
 * long way away from node 1 (02), with node 2 (05) bridging the gap between it and the master node.
 *
 * To use the sketch, upload it to two or more units and set the NODE_ADDRESS below. If configuring only a few
 * units, set the addresses to 0,1,3,5... to configure all nodes as children to each other. If using many nodes,
 * it is easiest just to increment the NODE_ADDRESS by 1 as the sketch is uploaded to each device.
 */
#include <avr/pgmspace.h>
#include <RF24Network.h>
#include <RF24.h>
#include <SPI.h>
#include "printf.h"
/***********************************************************************
************* Set the Node Address *************************************
/***********************************************************************/
// These are the Octal addresses that will be assigned
const uint16_t node_address_set[10] = { 00, 02, 05, 012, 015, 022, 025, 032, 035, 045 };
 
// 0 = Master
// 1-2 (02,05)   = Children of Master(00)
// 3,5 (012,022) = Children of (02)
// 4,6 (015,025) = Children of (05)
// 7   (032)     = Child of (02)
// 8,9 (035,045) = Children of (05)
uint8_t NODE_ADDRESS = 2;  // Use numbers 0 through to select an address from the array
/***********************************************************************/
/***********************************************************************/
RF24 radio(7,8);                              // CE & CS pins to use (Using 7,8 on Uno,Nano)
RF24Network network(radio); 
uint16_t this_node;                           // Our node address
const unsigned long interval = 1000; // ms       // Delay manager to send pings regularly.
unsigned long last_time_sent;
const short max_active_nodes = 10;            // Array of nodes we are aware of
uint16_t active_nodes[max_active_nodes];
short num_active_nodes = 0;
short next_ping_node_index = 0;
bool send_T(uint16_t to);                      // Prototypes for functions to send & handle messages
bool send_N(uint16_t to);
bool send_P(uint16_t to);
void handle_P(RF24NetworkHeader& header);
void handle_T(RF24NetworkHeader& header);
void handle_N(RF24NetworkHeader& header);
void add_node(uint16_t node);
struct dataStruct {
  unsigned long _micros;  // to save response times
  int Xposition;          // The Joystick position values
  int Yposition;
  bool switchOn;          // The Joystick push-down switch
} myData;                 // This can be accessed in the form:  myData.Xposition  etc.


//Atmega328p based Arduino code (should work withouth modifications with Atmega168/88), tested on RBBB Arduino clone by Modern Device:
const byte joysticYA = A0; //Analog Jostick Y axis
const byte joysticXA = A1; //Analog Jostick X axis

const byte controllerFA = 9; //PWM FORWARD PIN for OSMC Controller A (left motor)
const byte controllerRA = 6;  //PWM REVERSE PIN for OSMC Controller A (left motor)
const byte controllerFB = 3;  //PWM FORWARD PIN for OSMC Controller B (right motor)
const byte controllerRB = 5;  //PWM REVERSE PIN for OSMC Controller B (right motor)
const byte disablePin = 2; //OSMC disable, pull LOW to enable motor controller

int analogTmp = 0; //temporary variable to store 
int throttle, directn = 0; //throttle (Y axis) and direction (X axis) 

//Exponential smoothing parameters
float leftMotorPred = 0.0;
float rightMotorPred = 0.0;
float alpha = .25;  // lower number reduces sensitivity and decreases filter response
float beta = .75;   // the sum of these two parameters must equal 1.0 

int leftMotor,leftMotorScaled = 0; //left Motor helper variables
float leftMotorScale = 0;

int rightMotor,rightMotorScaled = 0; //right Motor helper variables
float rightMotorScale = 0;

float maxMotorScale = 0; //holds the mixed output scaling factor

int deadZone = 10; //jostick dead zone 



void setup(){

  Serial.begin(9600);
  Serial.println( __FILE__ );  // print out the file name so we know whats in the Ardunio
  
  myData.Xposition = 0;
  myData.Yposition = 0;
  myData.switchOn = false;
//  Serial.begin(9600);
  printf_begin();
  Serial.print("**************  START  ********************");
  printf_P(PSTR("\n\rRF24Network/examples/meshping/\n\r"));
  this_node = node_address_set[NODE_ADDRESS];            // Which node are we?
  
//  SPI.begin();                                           // Bring up the RF network
//  radio.begin();
//  radio.setPALevel(RF24_PA_HIGH);
//  network.begin(/*channel*/ 100, /*node address*/ this_node );
}
void loop(){
    
//  network.update();                                      // Pump the network regularly
//   while ( network.available() )  {                      // Is there anything ready for us?
//     
//    RF24NetworkHeader header;                            // If so, take a look at it
//    network.peek(header);
//    
//      switch (header.type){                              // Dispatch the message to the correct handler.
//        case 'T': handle_T(header); break;
//        case 'N': handle_N(header); break;
//        case 'P': handle_P(header); break;       
//        default:  printf_P(PSTR("*** WARNING *** Unknown message type %c\n\r"),header.type);
//                  network.read(header,0,0);
//                  break;
//      };
//    }
//  
//  unsigned long now = millis();                         // Send a ping to the next node every 'interval' ms
//  if ( now - last_time_sent >= interval ){
//    last_time_sent = now;
//    uint16_t to = 00;                                   // Who should we send to? By default, send to base
//    
//    
//    if ( num_active_nodes ){                            // Or if we have active nodes,
//        to = active_nodes[next_ping_node_index++];      // Send to the next active node
//        if ( next_ping_node_index > num_active_nodes ){ // Have we rolled over?
//            next_ping_node_index = 0;                   // Next time start at the beginning
//            to = 00;                                    // This time, send to node 00.
//        }
//    }
//    bool ok;
//    
//    if ( this_node > 00 || to == 00 ){                    // Normal nodes send a 'T' ping
//        ok = send_T(to);   
//    }else{                                                // Base node sends the current active nodes out
//        ok = send_N(to);
//    }
//    
//    if (ok){                                              // Notify us of the result
//        printf_P(PSTR("%lu: APP Send ok\n\r"),millis());
//        Serial.println("  |  ");
//        Serial.println(myData.Xposition);
//        Serial.println(myData.Yposition);
//
//  //aquire the analog input for Y  and rescale the 0..1023 range to -255..255 range
//  analogTmp = myData.Yposition;
//  throttle = (512-analogTmp)/2;
//
//  delayMicroseconds(100);
//  //...and  the same for X axis
//  analogTmp = myData.Xposition;
//  direction = -(512-analogTmp)/2;

// dummy in some throttle and direction numbers 
  throttle = 100;
  directn = -20;

  //mix throttle and direction
  leftMotor = throttle+directn;
  rightMotor = throttle-directn;

  //print the initial mix results
  Serial.print("LIN:"); Serial.print( leftMotor, DEC);
  Serial.print(", RIN:"); Serial.print( rightMotor, DEC);
  
// Exponential smoothing to try to reduce the sensitivity and jerkiness of the robot motion
leftMotorPred = alpha * leftMotor + beta * leftMotorPred;
rightMotorPred = alpha * rightMotor + beta * rightMotorPred;
leftMotor = leftMotorPred;
rightMotor = rightMotorPred;

  //calculate the scale of the results in comparision base 8 bit PWM resolution
  leftMotorScale =  leftMotor/255.0;
  leftMotorScale = abs(leftMotorScale);
  rightMotorScale =  rightMotor/255.0;
  rightMotorScale = abs(rightMotorScale);

  Serial.print("| LSCALE:"); Serial.print( leftMotorScale,2);
  Serial.print(", RSCALE:"); Serial.print( rightMotorScale,2);

  //choose the max scale value if it is above 1
  maxMotorScale = max(leftMotorScale,rightMotorScale);
  maxMotorScale = max(1,maxMotorScale);

  //and apply it to the mixed values
  leftMotorScaled = constrain(leftMotor/maxMotorScale,-255,255);
  rightMotorScaled = constrain(rightMotor/maxMotorScale,-255,255);

  Serial.print("| LOUT:"); Serial.print( leftMotorScaled);
  Serial.print(", ROUT:"); Serial.print( rightMotorScaled);

  Serial.print(" |");

  //apply the results to appropriate uC PWM outputs for the LEFT motor:
  if(abs(leftMotorScaled)>deadZone)
  {

    if (leftMotorScaled > 0)
    {
      Serial.print(" FL: ");
      Serial.print(abs(leftMotorScaled),DEC);

      analogWrite(controllerRA,0);
      analogWrite(controllerFA,abs(leftMotorScaled));            
    }
    else 
    {
      Serial.print(" RL: ");
      Serial.print(abs(leftMotorScaled),DEC);

      analogWrite(controllerFA,0);
      analogWrite(controllerRA,abs(leftMotorScaled));  
    }
  }  
  else 
  {
  Serial.print("IDLE");
  analogWrite(controllerFA,0);
  analogWrite(controllerRA,0);
  } 

  //apply the results to appropriate uC PWM outputs for the RIGHT motor:  
  if(abs(rightMotorScaled)>deadZone)
  {

    if (rightMotorScaled > 0)
    {
      Serial.print(" FR: ");
      Serial.print(abs(rightMotorScaled),DEC);

      analogWrite(controllerRB,0);
      analogWrite(controllerFB,abs(rightMotorScaled));            
    }
    else 
    {
      Serial.print(" RR: ");
      Serial.print(abs(rightMotorScaled),DEC);

      analogWrite(controllerFB,0);
      analogWrite(controllerRB,abs(rightMotorScaled));  
    }
  }  
  else 
  {
  Serial.print("IDLE");
  analogWrite(controllerFB,0);
  analogWrite(controllerRB,0);
  } 

  Serial.println("");

  //To do: throttle change limiting, to avoid radical changes of direction for large DC motors

  delay(10);


        
//    else{
//        printf_P(PSTR("%lu: APP Send failed\n\r"),millis());
//        last_time_sent -= 100;                            // Try sending at a different time next time
//    }
//  }
//  delay(50);                          // Delay to allow completion of any serial printing
//  if(!network.available()){
//      network.sleepNode(2,0);         // Sleep this node for 2 seconds or a payload is received (interrupt 0 triggered), whichever comes first
//  }
}
/**
 * Send a 'T' message, the current time
 */
bool send_T(uint16_t to)
{
  RF24NetworkHeader header(/*to node*/ to, /*type*/ 'T' /*Time*/);
  
  // The 'T' message that we send is just a ulong, containing the time
  unsigned long message = millis();
  printf_P(PSTR("---------------------------------\n\r"));
  printf_P(PSTR("%lu: APP Sending %lu to 0%o...\n\r"),millis(),message,to);
  return network.write(header,&message,sizeof(unsigned long));
}
/**
 * Send a 'P' message, the joystick x, y coordinates and switch position
 */
bool send_P(uint16_t to)
{
  RF24NetworkHeader header(/*to node*/ to, /*type*/ 'P' /*joystick data*/);
  
  // The 'T' message that we send is just a ulong, containing the time
  // The 'P' message will be joystick data
 // unsigned long message = millis();
  printf_P(PSTR("---------------------------------\n\r"));
  printf_P(PSTR("%lu: APP Sending %lu to 0%o...\n\r"),millis(),myData,to);
  return network.write(header,&myData,sizeof(myData));
}
/**
 * Send an 'N' message, the active node list
 */
bool send_N(uint16_t to)
{
  RF24NetworkHeader header(/*to node*/ to, /*type*/ 'N' /*Time*/);
  
  printf_P(PSTR("---------------------------------\n\r"));
  printf_P(PSTR("%lu: APP Sending active nodes to 0%o...\n\r"),millis(),to);
  return network.write(header,active_nodes,sizeof(active_nodes));
}
/**
 * Handle a 'T' message
 * Add the node to the list of active nodes
 */
void handle_T(RF24NetworkHeader& header){
  unsigned long message;                                                                      // The 'T' message is just a ulong, containing the time
  network.read(header,&message,sizeof(unsigned long));
  printf_P(PSTR("%lu: APP Received %lu from 0%o\n\r"),millis(),message,header.from_node);
  if ( header.from_node != this_node || header.from_node > 00 )                                // If this message is from ourselves or the base, don't bother adding it to the active nodes.
    add_node(header.from_node);
}
/**
 * Handle a 'P' message
 * Add the node to the list of active nodes
 */
//void handle_P(RF24NetworkHeader& header){
////  unsigned long message;                                                                      // The 'T' message is just a ulong, containing the time
//  network.read(header,&myData,sizeof(myData));
//  printf_P(PSTR("%lu: APP Received %lu from 0%o\n\r"),millis(),myData,header.from_node);
//  Serial.println();
//  Serial.print("Header: ");
//  Serial.println(&myData);
//  
//  if ( header.from_node != this_node || header.from_node > 00 )                                // If this message is from ourselves or the base, don't bother adding it to the active nodes.
//    add_node(header.from_node);
//}
//
///**
// * Handle an 'N' message, the active node list
// */
//void handle_N(RF24NetworkHeader& header)
//{
//  static uint16_t incoming_nodes[max_active_nodes];
//  network.read(header,&incoming_nodes,sizeof(incoming_nodes));
//  printf_P(PSTR("%lu: APP Received nodes from 0%o\n\r"),millis(),header.from_node);
//  int i = 0;
//  while ( i < max_active_nodes && incoming_nodes[i] > 00 )
//    add_node(incoming_nodes[i++]);
//}
///**
// * Add a particular node to the current list of active nodes
// */
//void add_node(uint16_t node){
//  
//  short i = num_active_nodes;                                    // Do we already know about this node?
//  while (i--)  {
//    if ( active_nodes[i] == node )
//        break;
//  }
//  
//  if ( i == -1 && num_active_nodes < max_active_nodes ){         // If not, add it to the table
//      active_nodes[num_active_nodes++] = node; 
//      printf_P(PSTR("%lu: APP Added 0%o to list of active nodes.\n\r"),millis(),node);
//  }
//}
