#include <LiquidCrystal.h>

LiquidCrystal lcd(7, 6, 5, 4, 3, 2);

#define MQPin A0
#define buzzer 1

void setup() {
   lcd.begin(16, 2);
   pinMode(MQPin, INPUT_PULLUP);
   pinMode(buzzer, OUTPUT);
    lcd.setCursor(5, 0);
    lcd.print("GAS");
    lcd.setCursor(3, 1);
    lcd.print("DETECTOR");
    delay(1000);
    lcd.clear();
}

void loop() {

int gas_value = digitalRead(MQPin);

if(gas_value==HIGH)
{
  digitalWrite(buzzer, HIGH);
  lcd.setCursor(6, 0);
  lcd.print("GAS");
   lcd.setCursor(3, 1);
  lcd.println("DETECTED");
  lcd.print(gas_value);
  delay(200);
  lcd.clear();
  delay(200);
  
}
else
{
 lcd.print(gas_value);
 lcd.clear();
 digitalWrite(buzzer, LOW); 
}
  

}
