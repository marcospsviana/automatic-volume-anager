#include <Servo.h>

#define servo0 A0
#define servo1 A1
#define servo2 A2
#define servo3 A3
#define servo4 A4
#define servo5 0
#define servo6 1
#define servo7 2
#define servo8 3
#define servo9 4
#define servo10 5
#define servo11 6

Servo servoOut;

void setup(){
    Serial.begin(9600);
    pinMode(servoOut, OUTPUT);
}