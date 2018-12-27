#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>

Adafruit_MMA8451 mma = Adafruit_MMA8451();

void setup(void) {
  Serial.begin(9600); // Set up serial port
  // Verify that the accelerometer is available
  if (! mma.begin()) {
    Serial.println("Couldnt start");
    while (1);
  }
  //Set accelerometer to +-2g mode (available modes: 2g,4g,8g)  
  mma.setRange(MMA8451_RANGE_2_G);
}

void loop() {
  /* Get a new sensor event */ 
  sensors_event_t event; 
  mma.getEvent(&event); // get data from accelerometer
  // print data to serial port - format: x,y
  Serial.print(event.acceleration.x); Serial.print(",");
  Serial.print(event.acceleration.y);
  Serial.println();
  delay(50);  // sleep for 50 milliseconds (1/20th sec)
}
