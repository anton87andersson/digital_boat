// Testprogram för att läsa av motortempraturen på en B20/AQ130D med orginal-givare.

#include <Adafruit_LiquidCrystal.h>

float calculateTemperature(float resistance) {
    // Temperatur-resistanspunkter
    float R[] = {650.0, 250.0, 80.0};
    float T[] = {20.0, 50.0, 80.0};
    
    // Beräkna polynomet som går genom punkterna
    float a0 = T[0];
    float a1 = (T[1] - T[0]) / (R[1] - R[0]);
    float a2 = ((T[2] - T[1]) / (R[2] - R[1]) - a1) / (R[2] - R[0]);
    
    // Beräkna temperaturen med det polynomet
    float temperature = a0 + a1 * (resistance - R[0]) + a2 * (resistance - R[0]) * (resistance - R[1]);
    return temperature;
}


float calculateBar(float resistance) {
    // Temperatur-resistanspunkter
    float R[] = {0.0, 5.0, 10.0};
    float T[] = {10.0, 90.0, 184.0};
    
    // Beräkna polynomet som går genom punkterna
    float a0 = T[0];
    float a1 = (T[1] - T[0]) / (R[1] - R[0]);
    float a2 = ((T[2] - T[1]) / (R[2] - R[1]) - a1) / (R[2] - R[0]);
    
    // Beräkna temperaturen med det polynomet
    float temperature = a0 + a1 * (resistance - R[0]) + a2 * (resistance - R[0]) * (resistance - R[1]);
    return temperature;
}


int analogPin = 0;
int raw = 0;
int Vin = 5;
float Vout = 0;
float R1 = 1000;
float R2 = 0;
float buffer = 0;

int analogPin_2 = 1;
int raw_2 = 0;
int Vin_2 = 5;
float Vout_2 = 0;
float R3 = 1000;
float R4 = 0;
float buffer = 0;



int seconds = 0;

Adafruit_LiquidCrystal lcd_1(0);

void setup()
{
  pinMode(8, OUTPUT); // green light 
  pinMode(7, OUTPUT); // Red light
  lcd_1.begin(16, 2);
  lcd_1.print("Temp motor: ");
  Serial.begin(9600);
}

void loop()
{
  // Motortemp
  raw = analogRead(analogPin);
  if(raw){
    
    buffer = raw * Vin;
    Vout = (buffer)/1024.0;
    buffer = (Vin/Vout) - 1;
    R2= R1 * buffer;
    
    lcd_1.setCursor(8, 1);
    lcd_1.write(B11011111);
    lcd_1.setCursor(0, 1);

    
    float temperature = calculateTemperature(R2);
    lcd_1.print(temperature);
    
    //Serial.println("Ohm: ");
    //Serial.println(R2);
    
    if (temperature < 90){
      digitalWrite(7, LOW); // Stäng av röd lampa
      digitalWrite(8, HIGH); // Grön lampa, allt ok
    }
    else{
      digitalWrite(8, LOW); // Stäng av grön lampa
      digitalWrite(7, HIGH); // Röd lampa, för hög temp
    }
    
    // Oljetryck
	
    raw_2 = analogRead(analogPin_2);
  	if(raw_2){
    
    buffer_2 = raw_2 * Vin_2;
    Vout_2 = (buffer_2)/1024.0;
    buffer_2 = (Vin_2/Vout_2) - 1;
    R4= R3 * buffer;
    
    //lcd_1.setCursor(8, 1);
    //lcd_1.write(B11011111);
    //lcd_1.setCursor(0, 1);

    
    float oil_bar = calculateBar(R3);
    //lcd_1.print(temperature);
    
    Serial.println("Oljetryck: ");
    Serial.println(oil_bar);
    
    
    
 
    
  }
  delay(100); // Wait for 100 millisecond(s)
}
