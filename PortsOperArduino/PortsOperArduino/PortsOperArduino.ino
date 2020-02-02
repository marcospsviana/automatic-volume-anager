
/*   **********    AUTOR MARCOS PAULO SILVA VIANA PROJETO COOLBAGSAFE-RENTLOCKER  *************************************** 
        DEFININDO AS PORTAS LED_OPER ( OUTPUT )SERAO ESTADO DE OPERACAO QUANDO ATIVO ELAS IRAO PISCAR CONFORME A PORTA
        DESIGNADA ESTIVER EM OPERACAO ||  
        LED_STATUS ( OUTPUT ) O ESTADO EM QUE A PORTA SE ENCONTRA OCUPADO OU LIVRE, LIVRE = LOW , OCUPADO = HIGH
        LED_SENSOR  ( INPUT ) RESPONSAVEIS POR DETECTAR SE A PORTA ESTA OU NAO FECHADA 
     ******************************************************************************************************************** */    
#include <Arduino.h>
#include "Servo.h"

#define LED_OPER_2          2
#define LED_STATUS_BUSY_3   3
#define LED_STATUS_FREE_4   4
#define LED_OPER_5          5
#define LED_STATUS_BUSY_6   6
#define LED_STATUS_FREE_7   7
#define LED_OPER_8          8
#define LED_STATUS_BUSY_9   9
#define LED_STATUS_FREE_10  10

#define SENSOR_11           11
#define SENSOR_12           12
#define SENSOR_13           13


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

    pinMode(2, OUTPUT);
    pinMode(3, OUTPUT);
    pinMode(LED_STATUS_FREE_4, OUTPUT);
    pinMode(5, OUTPUT);
    pinMode(6, OUTPUT);
    pinMode(LED_STATUS_FREE_7, OUTPUT);
    pinMode(8, OUTPUT);
    pinMode(9, OUTPUT);
    pinMode(LED_STATUS_FREE_10, OUTPUT);

    pinMode(11, INPUT);
    pinMode(12, INPUT);
    pinMode(13, INPUT);

    digitalWrite(2, LOW);
    digitalWrite(3, LOW);
    digitalWrite(LED_STATUS_FREE_4, HIGH);
    digitalWrite(5, LOW);
    digitalWrite(6, LOW);
    digitalWrite(LED_STATUS_FREE_7, HIGH);
    digitalWrite(8, LOW);
    digitalWrite(9, LOW);
    digitalWrite(LED_STATUS_FREE_10, HIGH);

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
 
    if(Serial.available() > 0)
    {
      String recebido = leStringSerial();
      if (recebido == "A0:abre")
      {
        for(pos = 0; pos <= 180; pos += 1)
          {
            servo_A0.write(pos);
            delay(15);
          }
      }
      if (recebido == "A0:fecha")
      {
        for(pos = 180; pos >= 0; pos -= 1)
          {
          servo_A0.write(pos);
          delay(15);
          }
      }
      if(recebido == "A1:abre")
      {
        for(pos = 0; pos <= 180; pos += 1)
          {
            servo_A1.write(pos);
            delay(15);
          }
      }
      if (recebido == "A1:fecha")
      {
        for(pos = 180; pos >= 0; pos -= 1)
          {
          servo_A1.write(pos);
          delay(15);
          }
      }
      if(recebido == "A2:abre")
      {
        for(pos = 0; pos <= 180; pos += 1)
          {
            servo_A2.write(pos);
            delay(15);
          }
      }
      if (recebido == "A2:fecha")
      {
        for(pos = 180; pos >= 0; pos -= 1)
          {
          servo_A2.write(pos);
          delay(15);
          }
      }
    }
}
