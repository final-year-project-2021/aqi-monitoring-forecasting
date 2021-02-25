
void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(A0, INPUT);
pinMode(A1, INPUT);
}

void loop() {
  int data = digitalRead(A0);
  int data1 = digitalRead(A1);
  Serial.print("CO=");
  Serial.println(data);
  Serial.print("H2=");
  Serial.println(data1);
  delay(100);
  
}
