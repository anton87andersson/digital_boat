// Define analog inputs
#define ANALOG_IN_PIN_1 A0
#define ANALOG_IN_PIN_2 A2
#define ANALOG_IN_PIN_3 A3  // Added line for the third analog input
 
// Floats for ADC voltage & Input voltage
float adc_voltage_1 = 0.0;
float in_voltage_1 = 0.0;
float adc_voltage_2 = 0.0;
float in_voltage_2 = 0.0;
float adc_voltage_3 = 0.0;  // Added line for the third ADC voltage
float in_voltage_3 = 0.0;  // Added line for the third input voltage
 
// Floats for resistor values in divider (in ohms)
float R1 = 30000.0;
float R2 = 7500.0;
 
// Float for Reference Voltage
float ref_voltage = 5.0;
 
// Integer for ADC values
int adc_value_1 = 0;
int adc_value_2 = 0;
int adc_value_3 = 0;  // Added line for the third ADC value
 
void setup() {
   // Setup Serial Monitor
   Serial.begin(9600);
   Serial.println("DC Voltage Test");
}
 
void loop() {
   // Read the Analog Inputs
   adc_value_1 = analogRead(ANALOG_IN_PIN_1);
   adc_value_2 = analogRead(ANALOG_IN_PIN_2);
   adc_value_3 = analogRead(ANALOG_IN_PIN_3);  // Added line for reading the third analog input
   
   // Determine voltage at ADC inputs
   adc_voltage_1 = (adc_value_1 * ref_voltage) / 1024.0;
   adc_voltage_2 = (adc_value_2 * ref_voltage) / 1024.0;
   adc_voltage_3 = (adc_value_3 * ref_voltage) / 1024.0;  // Added line for calculating the third ADC voltage
   
   // Calculate voltage at divider inputs
   in_voltage_1 = adc_voltage_1 / (R2 / (R1 + R2));
   in_voltage_2 = adc_voltage_2 / (R2 / (R1 + R2));
   in_voltage_3 = adc_voltage_3 / (R2 / (R1 + R2));  // Added line for calculating the third input voltage
 
   unsigned int x = 0;
   float AcsValue = 0.0, Samples = 0.0, AvgAcs = 0.0, AcsValueF = 0.0;
 
   for (int x = 0; x < 150; x++) { // Get 150 samples
      AcsValue = analogRead(A1);     // Read current sensor values   
      Samples = Samples + AcsValue;  // Add samples together
      delay(3); // Let ADC settle before next sample 3ms
   }
   AvgAcs = Samples / 150.0; // Taking Average of Samples
 
   AcsValueF = (2.5 - (AvgAcs * (5.0 / 1024.0))) / 0.066;
 
   Serial.print(in_voltage_1, 2);
   Serial.print(" : ");
   Serial.print(in_voltage_2, 2);
   Serial.print(" : ");
   Serial.print(in_voltage_3, 2);  // Added line for printing the third input voltage with 2 decimal places
   Serial.print(" : ");
   Serial.println(AcsValueF, 4); // Print the read current on Serial monitor
 
   delay(5000); // 5 seconds delay
}