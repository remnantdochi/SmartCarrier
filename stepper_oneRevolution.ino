/* 
 Stepper Motor Control - speed control

 This program drives a unipolar or bipolar stepper motor.
 The motor is attached to digital pins 8 - 11 of the Arduino.
 A potentiometer is connected to analog input 0.

 The motor will rotate in a clockwise direction. The higher the potentiometer value,
 the faster the motor speed. Because setSpeed() sets the delay between steps,
 you may notice the motor is less responsive to changes in the sensor value at
 low speeds.
 //오른쪽 바퀴가 + , 왼쪽 바퀴가 -
 Created 30 Nov. 2009
 Modified 28 Oct 2010
 by Tom Igoe

 */

#include <Stepper.h>

int stepsPerRevolution = 200;  // 360/1.8이다. 한바퀴당 200스텝인 것.
// for your motor


// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);

int stepCount = 0;  // number of steps the motor has taken
void SmartCar_Go();
void SmartCar_Back();
void SmartCar_Stop();
void checkcommand();
void Obstacle_Check();
void Distance_Measurement();
void moveCar();

char prev_command;
char command;
int come_in=1;


void setup() {
  Serial.begin(9600);
  // nothing to do inside the setup
  Serial.setTimeout(50);
}

void loop() {
  
  checkcommand();
  moveCar();
  

}

void checkcommand(){
  if (Serial.available())   // PC와의 시리얼통신으로 부터 받은 값이 있는지 판단
  {
    command = Serial.read();    // 명령 저장
    Serial.println("Recived command");
  }
  else if (prev_command == 'r' || prev_command == 'l'){
    command = 'g';
  }
  else{
    command = prev_command;
  }
  
    
}


void moveCar(){
  
  
    if(command == 'g'){// 전진 명령
        
        SmartCar_Go();
        
    
    }
      
    else if(command == 'b'){          // 후진 명령
      SmartCar_Back();
        
      }
    
    else if(command == 's'){          // 정지 명령
      
      SmartCar_Stop();
    
    }
    else if(command == 'l'){// 좌회전 명령 //0도

      
      SmartCar_Left();
    }
      
    
    else if(command == 'r'){          // 우회전 명령//180도
     
      SmartCar_Right();
    
    }
    else{      
    }
    
  
}

void SmartCar_Go(){        // 전진
    
    Serial.println("Forward");
    // read the sensor value:
    int sensorReading = 50;
    // map it to a range from 0 to 100:
    int motorSpeed = map(sensorReading, 0, 1023, 0, 100);
    // set the motor speed:
    if (motorSpeed >= 0) {
      myStepper.setSpeed(70);
      // step 1/100 of a revolution:
      myStepper.step(-stepsPerRevolution);
    }
    Serial.println("End forward");
    
   prev_command = 'g';
}
void SmartCar_Back(){        // 후진
  if (prev_command == 'b') {
      return;
    }

    Serial.println("Backward");
    // read the sensor value:
    int sensorReading = analogRead(A0);
    // map it to a range from 0 to 100:
    int motorSpeed = map(sensorReading, 0, 1023, 0, 100);
    // set the motor speed:
    if (motorSpeed > 0) {
      myStepper.setSpeed(motorSpeed);
      // step 1/100 of a revolution:
      myStepper.step(stepsPerRevolution);
    }
    prev_command = 'b';
}
void SmartCar_Stop(){       // 정지0
  // read the sensor value:
  Serial.println("Stop");
  int sensorReading = analogRead(A0);
  // map it to a range from 0 to 100:
  int motorSpeed = map(sensorReading, 0, 1023, 0, 100);
  // set the motor speed:
  myStepper.setSpeed(0);
  // step 1/100 of a revolution:
  myStepper.step(0);
  delay(1000);
  prev_command = 's';
}

void SmartCar_Left()  // 좌회전
{   Serial.println("Left");
    // read the sensor value:
    int sensorReading = 50;
    // map it to a range from 0 to 100:
    int motorSpeed = map(sensorReading, 0, 1023, 0, 100);
    // set the motor speed:
    if (motorSpeed >= 0) {
      myStepper.setSpeed(50);
      // step 1/100 of a revolution:
      myStepper.step(-stepsPerRevolution/2);
    }
  
  prev_command = 'l';
}
void SmartCar_Right() // 우회전
{
    Serial.println("Right");
    // read the sensor value:
    int sensorReading = 50;
    // map it to a range from 0 to 100:
    int motorSpeed = map(sensorReading, 0, 1023, 0, 100);
    // set the motor speed:
    if (motorSpeed >= 0) {
      myStepper.setSpeed(100);
      // step 1/100 of a revolution:
      myStepper.step(-stepsPerRevolution*1.6);
    }
  prev_command = 'r';
}
