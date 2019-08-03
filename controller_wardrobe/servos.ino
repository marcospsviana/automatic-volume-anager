#include <Servo.h>

Servo servo_A0;
Servo servo_A1;
Servo servo_A2;
Servo servo_A3;
Servo servo_A4;
Servo servo_0;
Servo servo_1;
Servo servo_2;
Servo servo_3;
Servo servo_4;
Servo servo_5;
Servo servo_6;

int pos = 0;

void setup(){
    Serial.begin(9600);
    servo_A0.atach(A0);
    servo_A1.atach(A1);
    servo_A2.atach(A2);
    servo_A3.atach(A3);
    servo_A4.atach(A4);
    servo_0.atach(0);
    servo_1.atach(1);
    servo_2.atach(2);
    servo_3.atach(3);
    servo_4.atach(4);
    servo_5.atach(5);
    servo_6.atach(6);

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