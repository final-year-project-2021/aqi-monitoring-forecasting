#include "DHT.h"

DHT dht(2, DHT11);

void setup(){
  Serial.begin(9600);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  dht.begin();
}

void loop() {
  int data = digitalRead(A0);
  int data1 = digitalRead(A1);
  float humid = dht.readHumidity();
  float temp = dht.readTemperature();
  
  Serial.print("CO=");
  Serial.println(data);
  Serial.print("H2=");
  Serial.println(data1);
  Serial.print("humidity=");
  Serial.println(humid);
  Serial.print("temperature=");
  Serial.println(temp);
  
  delay(1000);
  
}
