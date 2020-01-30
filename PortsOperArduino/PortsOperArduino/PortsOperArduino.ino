
/*   **********    AUTOR MARCOS PAULO SILVA VIANA PROJETO COOLBAGSAFE-RENTLOCKER  *************************************** 
        DEFININDO AS PORTAS LED_OPER ( OUTPUT )SERAO ESTADO DE OPERACAO QUANDO ATIVO ELAS IRAO PISCAR CONFORME A PORTA
        DESIGNADA ESTIVER EM OPERACAO ||  
        LED_STATUS ( OUTPUT ) O ESTADO EM QUE A PORTA SE ENCONTRA OCUPADO OU LIVRE, LIVRE = LOW , OCUPADO = HIGH
        LED_SENSOR  ( INPUT ) RESPONSAVEIS POR DETECTAR SE A PORTA ESTA OU NAO FECHADA 
     ******************************************************************************************************************** */    

#define LED_OPER_2 2
#define LED_STATUS_3 3
#define LED_OPER_4 4
#define LED_STATUS_5 5
#define LED_OPER_6 6
#define LED_STATUS_7 7

#define LED_SENSOR_8 8
#define LED_SENSOR_9 9
#define LED_SENSOR_10 10



void setup() {                
  // INICIALIZA OS PINOS DE SAIDA
  pinMode(LED_OPER_2,    OUTPUT); 
  pinMode(LED_STATUS_3,   OUTPUT);
  pinMode(LED_OPER_4,    OUTPUT); 
  pinMode(LED_STATUS_5,   OUTPUT);
  pinMode(LED_OPER_6,    OUTPUT); 
  pinMode(LED_STATUS_7,   OUTPUT);
  
  pinMode(LED_SENSOR_8,  INPUT);
  pinMode(LED_SENSOR_9,  INPUT);
  pinMode(LED_SENSOR_10, INPUT);
  
  // COLOCA TODOS EM NIVEL BAIXO
  digitalWrite(LED_OPER_2,   LOW); 
  digitalWrite(LED_STATUS_3, LOW);
  digitalWrite(LED_OPER_4,   LOW); 
  digitalWrite(LED_STATUS_5, LOW);
  digitalWrite(LED_OPER_6,   LOW); 
  digitalWrite(LED_STATUS_7, LOW);

   
}

void ledInOper(int led){

}
void loop() {
  
}
