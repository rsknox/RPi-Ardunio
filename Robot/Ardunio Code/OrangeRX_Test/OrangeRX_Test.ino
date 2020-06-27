byte pin4 = 4;
byte pin5 = 5;
byte pin6 = 6;
byte pin7 = 7;
byte pin8 = 8;
byte pin9 = 9;
 
int pwm_value_4;
int pwm_value_5;
int pwm_value_6;
int pwm_value_7;
int pwm_value_8;
int pwm_value_9;
 
void setup() {
  Serial.begin(9600);
  Serial.println( __FILE__ );
  Serial.println( __DATE__ );
  Serial.println( __TIME__ );
  pinMode(pin4, INPUT);
  pinMode(pin5, INPUT);
  pinMode(pin6, INPUT);
  pinMode(pin7, INPUT);
  pinMode(pin8, INPUT);
  pinMode(pin9, INPUT);
}
 
void loop() {
  pwm_value_4 = pulseIn(pin4, HIGH);
  pwm_value_5 = pulseIn(pin5, HIGH);
  pwm_value_6 = pulseIn(pin6, HIGH);
  pwm_value_7 = pulseIn(pin7, HIGH);
  pwm_value_8 = pulseIn(pin8, HIGH);
  pwm_value_9 = pulseIn(pin9, HIGH);
  String pv4 = String(pwm_value_4);
  String pv5 = String(pwm_value_5);
  String pv6 = String(pwm_value_6);
  String pv7 = String(pwm_value_7);
  String pv8 = String(pwm_value_8);
  String pv9 = String(pwm_value_9);
  String psrg = ("p4,T: " + pv4 + " p5,A: " + pv5 + " p6,E: " + pv6 + " p7,R: " + pv7 + " p8,G: " + pv8 + " p9,A1: " + pv9);
  Serial.println(psrg);
}
