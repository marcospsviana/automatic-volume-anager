void setup()
{
  char8_t listPin[18] = {"A0", "A1", "A2", "A3", "A4", "A5", "0", "1", "2", "3", "4","5","6","7","8","9","10","11","12","13"}
  for( int i = 0; i = 18; i++;){
    pinMode(listPin[i], OUTPUT);
  }
  char16_t entrada;
  Serial.begin(9600);

}
void lerDado(port, dado){

}
void loop()
{
  while (Serial.avaliable() > 0)
  {
    entrada = Serial.read();
    if (entrada == "0101"){
      digitalWrite(listPin, 1);
    }
    else if (entrada == "desliga")
    {
      digitalWrite(listPin, 0)
    }
    
  }
  
  
}
