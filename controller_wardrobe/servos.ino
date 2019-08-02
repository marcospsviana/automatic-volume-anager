#include <Servo.h>

Servo servo;
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servo6;
Servo servo7;
Servo servo8;
Servo servo9;
Servo servo10;
Servo servo11;

int pos = 0;

void setup(){
    Serial.begin(9600);
    servo.atach(A0);
    servo1.atach(A1);
    servo2.atach(A2);
    servo3.atach(A3);
    servo4.atach(A4);
    servo5.atach(0);
    servo6.atach(1);
    servo7.atach(2);
    servo8.atach(3);
    servo9.atach(4);
    servo10.atach(5);
    servo11.atach(6);

}
void controle(comando, servoport){
if (comando == 'abrir'){
    for(pos = 0; pos <= 180; pos += 1;){
        servoport.write(pos);
        delay(15);
    }
else if (commando == "fechar"){
    for(pos = 0; pos >= 0; pos -= 1;){
        servoport.write(pos);
        delay(15);
    }
}

}
}
void loop(){

}