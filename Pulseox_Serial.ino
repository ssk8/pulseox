#include <SparkFun_Bio_Sensor_Hub_Library.h>
#include <Wire.h>

int resPin = 4;
int mfioPin = 5;

SparkFun_Bio_Sensor_Hub bioHub(resPin, mfioPin); 

bioData sensor;  

void setup(){
  Wire.begin();
  int result = bioHub.begin();
  int error = bioHub.configBpm(MODE_TWO); 
  delay(4000);
}

void loop(){
    sensor = bioHub.readBpm();

    Serial.print(sensor.extStatus); 
    Serial.print(" ");
    Serial.print(sensor.heartRate);
    Serial.print(" ");
    Serial.print(sensor.oxygen); 
    Serial.print(" ");
    Serial.println(sensor.confidence); 

    delay(1000); 
}
