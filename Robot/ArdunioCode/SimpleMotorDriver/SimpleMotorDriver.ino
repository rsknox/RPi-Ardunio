void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println( __FILE__ );

  pinMode(A1, INPUT);
  pinMode(A2, INPUT);

  int pwm_value_1 = 0;
  int pwm_value_2 = 0;

  int deadZone = 60;
  
}

void loop() {
  // put your main code here, to run repeatedly:
  int deadZone = 60;
  int pwm_value_1 = pulseIn(A1, HIGH);
  int pwm_value_2 = pulseIn(A2, HIGH);
  String pv1 = String(pwm_value_1);
  String pv2 = String(pwm_value_2);
  String psrg = ("p A1, T: " + pv1 + " pA2 ,A: " + pv2);
  Serial.println(psrg);

  int throttle = 0.5 *(pwm_value_1 - 1500);
  if (throttle < 0){ throttle = 0;}
  int directn = 0.5 * (pwm_value_2 -1500);
  if (directn > 254){directn = 254;}
  if (directn < -254){directn = -254;}
  String Th = String(throttle);
  String Di = String(directn);
  String ip = ("T: " + Th + " D: " + Di);
  Serial.println(ip);

  //mix throttle and direction
  int leftMotor = throttle-directn;
  if (leftMotor < -254){leftMotor = -254;}
  if (leftMotor > 254){leftMotor = 254;}
  
  int rightMotor = throttle+directn;
  if (rightMotor < -254){rightMotor = -254;}
  if (rightMotor > 254){rightMotor = 254;}
  
  String LM = String (leftMotor);
  String RM = String (rightMotor);
  String motors = ("left motor: " + LM + " right motor: " + RM);
  Serial.println(motors);
  
//  analogWrite(6,125); //left forward
//  analogWrite(9,0); //left revers
//
//  analogWrite(5,125); //right forward
//  analogWrite(3,00);  //right reverse

    //apply the results to appropriate uC PWM outputs for the LEFT motor:
  if(abs(leftMotor)>deadZone)
  {

    if (leftMotor > 0)
    {
      Serial.print("F-left");
      Serial.print(abs(leftMotor),DEC);

      analogWrite(9,0);
      analogWrite(6,abs(leftMotor));            
    }
    else 
    {
      Serial.print("R-left");
      Serial.print(abs(leftMotor),DEC);

      analogWrite(6,0);
      analogWrite(9,abs(leftMotor));  
    }
  }  
  else 
  {
  Serial.print("IDLE");
  analogWrite(9,0);
  analogWrite(6,0);
  } 

  //apply the results to appropriate uC PWM outputs for the RIGHT motor:  
  if(abs(rightMotor)>deadZone)
  {

    if (rightMotor > 0)
    {
      Serial.print("F-right");
      Serial.print(abs(rightMotor),DEC);

      analogWrite(3,0);
      analogWrite(5,abs(rightMotor));            
    }
    else 
    {
      Serial.print("R-right");
      Serial.print(abs(rightMotor),DEC);

      analogWrite(5,0);
      analogWrite(3,abs(rightMotor));  
    }
  }  
  else 
  {
  Serial.print("IDLE");
  analogWrite(3,0);
  analogWrite(5,0);
  } 
}
