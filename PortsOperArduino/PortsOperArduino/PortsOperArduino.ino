
/*   **********    AUTOR MARCOS PAULO SILVA VIANA PROJETO COOLBAGSAFE-RENTLOCKER  *************************************** 
        DEFININDO AS PORTAS LED_OPER ( OUTPUT )SERAO ESTADO DE OPERACAO QUANDO ATIVO ELAS IRAO PISCAR CONFORME A PORTA
        DESIGNADA ESTIVER EM OPERACAO ||  
        LED_STATUS ( OUTPUT ) O ESTADO EM QUE A PORTA SE ENCONTRA OCUPADO OU LIVRE, LIVRE = LOW , OCUPADO = HIGH
        LED_STATUS_FREE O IDEM LED_STATUS MAS INVERTIDO LIVRE = HIGH, OCUPADO = LOW
        LED_SENSOR  ( INPUT ) RESPONSAVEIS POR DETECTAR SE A PORTA ESTA OU NAO FECHADA 
     ******************************************************************************************************************** */    
#include <Arduino.h>
#include "Servo.h"

#define LED_STATUS_OPER_A0   2
#define LED_STATUS_BUSY_A0   3
#define LED_STATUS_FREE_A0   4
#define LED_STATUS_OPER_A1   5
#define LED_STATUS_BUSY_A1   6
#define LED_STATUS_FREE_A1   7
#define LED_STATUS_OPER_A2   8
#define LED_STATUS_BUSY_A2   9
#define LED_STATUS_FREE_A2  10

#define SENSOR_A0           11
#define SENSOR_A1           12
#define SENSOR_A2           13
bool condicao = false;


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
int statusA0 = 0;
int statusA1 = 0;
int statusA2 = 0;

void setup() {
    Serial.begin(9600);
    servo_A0.attach(A0);
    servo_A1.attach(A1);
    servo_A2.attach(A2);
    //servo_A3.attach(A3);
    //servo_A4.attach(A4);

    // POSICIONA O SERVO NA POSICAO 0
    servo_A0.write(0);
    servo_A1.write(0);
    servo_A2.write(0);


    pinMode(LED_STATUS_OPER_A0, OUTPUT);
    pinMode(LED_STATUS_BUSY_A0, OUTPUT);
    pinMode(LED_STATUS_FREE_A0, OUTPUT);
    pinMode(LED_STATUS_OPER_A1, OUTPUT);
    pinMode(LED_STATUS_BUSY_A1, OUTPUT);
    pinMode(LED_STATUS_FREE_A1, OUTPUT);
    pinMode(LED_STATUS_OPER_A2, OUTPUT);
    pinMode(LED_STATUS_BUSY_A2, OUTPUT);
    pinMode(LED_STATUS_FREE_A2, OUTPUT);

    pinMode(SENSOR_A0, INPUT);
    pinMode(SENSOR_A1, INPUT);
    pinMode(SENSOR_A2, INPUT);

    digitalWrite(LED_STATUS_OPER_A0, LOW);
    digitalWrite(LED_STATUS_BUSY_A0, LOW);
    digitalWrite(LED_STATUS_FREE_A0, LOW); //LIVRE ATIVO
    digitalWrite(LED_STATUS_OPER_A1, LOW);
    digitalWrite(LED_STATUS_BUSY_A1, LOW);
    digitalWrite(LED_STATUS_FREE_A1, HIGH); //LIVRE ATIVO
    digitalWrite(LED_STATUS_OPER_A2, LOW);
    digitalWrite(LED_STATUS_BUSY_A2, LOW);
    digitalWrite(LED_STATUS_FREE_A2, HIGH);//LIVRE ATIVO
    


}
void piscaLed(){
        statusA0 = digitalRead(SENSOR_A0);
        if (statusA0 == 1){
            digitalWrite(LED_STATUS_OPER_A0, LOW);
            delay(300);
            digitalWrite(LED_STATUS_OPER_A0, HIGH);
            delay(300);}
        else{
          digitalWrite(LED_STATUS_OPER_A0, LOW);
        }
        statusA1 = digitalRead(SENSOR_A1);
        if (statusA1 == 1){
            digitalWrite(LED_STATUS_OPER_A1, LOW);
            delay(300);
            digitalWrite(LED_STATUS_OPER_A1, HIGH);
            delay(300);}
        else{
          digitalWrite(LED_STATUS_OPER_A1, LOW);
        } 
          
        statusA2 = digitalRead(SENSOR_A2);      
        if (statusA2 == 1){
            digitalWrite(LED_STATUS_OPER_A2, LOW);
            delay(600);
            digitalWrite(LED_STATUS_OPER_A2, HIGH);
            delay(600);}
        else{
          digitalWrite(LED_STATUS_OPER_A2, LOW);
        }

        
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
    delay(15);
  }
    
  Serial.print("Recebi: ");
  Serial.println(conteudo);
    
  return conteudo;
}

void loop(){
    //piscaLed();
    
 
    if(Serial.available() > 0)
    {
      String recebido = leStringSerial();
      if (recebido == "A0:abre:livre")
      {
        for(pos = 0; pos <= 180; pos += 1)
          {
            servo_A0.write(pos);
            delay(15);
          }
        digitalWrite(LED_STATUS_FREE_A0, HIGH);
        digitalWrite(LED_STATUS_BUSY_A0, LOW);
        condicao = true;
      }
      if (recebido == "A0:abre:ocupado")
      {
        for(pos = 0; pos <= 180; pos += 1)
          {
            servo_A0.write(pos);
            delay(15);
          }
        digitalWrite(LED_STATUS_OPER_A0, HIGH);
        digitalWrite(LED_STATUS_FREE_A0, LOW);
        digitalWrite(LED_STATUS_BUSY_A0, HIGH);
        
      }
      if (recebido == "A0:fecha:livre")
      {
        for(pos = 180; pos >= 0; pos -= 1)
          {
          servo_A0.write(pos);
          delay(15);
          }
        digitalWrite(LED_STATUS_FREE_A0, HIGH);
        digitalWrite(LED_STATUS_BUSY_A0, LOW);
      }
      if (recebido == "A0:fecha:ocupado")
      {
        for(pos = 180; pos >= 0; pos -= 1)
          {
          servo_A0.write(pos);
          delay(15);
          }
        digitalWrite(LED_STATUS_FREE_A0, LOW);
        digitalWrite(LED_STATUS_BUSY_A0, HIGH);
      }
     
      /*
      if (recebido == "A3:livre")
      {
        digitalWrite(LED_STATUS_FREE_A3, HIGH);
        digitalWrite(LED_STATUS_BUSY_A3, LOW);
      }
      if (recebido == "A3:ocupado")
      {
        digitalWrite(LED_STATUS_FREE_A3, LOW);
        digitalWrite(LED_STATUS_BUSY_A3, HIGH);
      }
      if (recebido == "A4:livre")
      {
        digitalWrite(LED_STATUS_FREE_A4, HIGH);
        digitalWrite(LED_STATUS_BUSY_A4, LOW);
      }
      if (recebido == "A4:ocupado")
      {
        digitalWrite(LED_STATUS_FREE_A4, LOW);
        digitalWrite(LED_STATUS_BUSY_A4, HIGH);
      }*/
    }
}
