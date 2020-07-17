#include <Arduino.h>
#include "Servo.h"
Servo servo_A0;
Servo servo_A1;
Servo servo_A2;
Servo servo_A3;
Servo servo_A4;
/*Servo servo_0;
Servo servo_1;
Servo servo_2;
Servo servo_3;
Servo servo_4;
Servo servo_5;
Servo servo_6;*/

int pos = 0;
int comando = 0;
int servoport = 0;

const int pin9 = 9;

void setup() {
    Serial.begin(9600);
    servo_A0.attach(A0);
    servo_A1.attach(A1);
    servo_A2.attach(A2);
    servo_A3.attach(A3);
    servo_A4.attach(A4);

    // POSICIONA O SERVO NA POSICAO 0
    servo_A0.write(0);
    servo_A1.write(0);
    servo_A2.write(0);

    // SETANDO PINOS DE ENTRADA
    pinMode(pin9, INPUT);
    

    //SETANDO PINOS DE SAÍDA

}
String leStringSerial(){
  String conteudo = "";
  char caractere;
  
  // Enquanto receber algo pela serial
  while(Serial.available() > 0) {
    // Lê byte da serial
    caractere = Serial.read();
    // Ignora caractere de quebra de linha
    if (caractere != '\n'){
      // Concatena valores
      conteudo.concat(caractere);
    }
    // Aguarda buffer serial ler próximo caractere
    delay(10);
  }
    
  Serial.print("Recebi: ");
  Serial.println(conteudo);
    
  return conteudo;
}



void loop(){
  int valuePort = digitalRead(pin9);
  if(valuePort == HIGH){
    for(pos = 180; pos >= 0; pos -= 1){
        servo_A0.write(pos);
        delay(15);
  }}
 
    if(Serial.available() > 0){
      String recebido = leStringSerial();
      if (recebido == "A0:abre"){
    for(pos = 0; pos <= 180; pos += 1){
        servo_A0.write(pos);
        delay(15);
    }}
    if (recebido == "A0:fecha"){
    for(pos = 180; pos >= 0; pos -= 1){
        servo_A0.write(pos);
        delay(15);
    }}
/*      }
if (comando == 1){
    for(pos = 0; pos <= 180; pos += 1){
        servo_A0.write(pos);
        delay(15);
    }
}
if (comando == 2){
    for(pos = 180; pos >= 0; pos -= 1){
        servo_A0.write(pos);
        delay(15);
    }
}

}*/}
delay(1000);
}
