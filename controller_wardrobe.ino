void setup()
{
  char8_t listPin[18] = {"A0", "A1", "A2", "A3", "A4", "A5", "0", "1", "2", "3", "4","5","6","7","8","9","10","11","12","13"}
  for( int i = 0; i = 18; i++;){
    pinMode(listPin[i], OUTPUT);
  }
  
  Serial.begin(9600);

}
void lerDado(port, dado){

}
void loop()
{
  digitalWrite(7, LOW);
  delay(1000); // Wait for 1000 millisecond(s)
  digitalWrite(7, HIGH);
  delay(1000); // Wait for 1000 millisecond(s)
  
}
