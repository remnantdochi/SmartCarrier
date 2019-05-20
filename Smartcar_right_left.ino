/* 이 소스는 에듀이노(Eduino)에 의해서 번역, 수정, 작성되었고 소유권 또한 에듀이노의 것입니다. 
 *  소유권자의 허락을 받지 않고 무단으로 수정, 삭제하여 배포할 시 법적인 처벌을 받을 수도 있습니다. 
 *  
 *  에듀이노 SmartCar 예제
 *  - 스마트 자동차 전진, 후진, 정지 명령 시리얼통신으로 제어하기 -
 *  
 *  PC와 USB케이블을 우노 보드와 연결한 상태에서 
 *  터미널을 통해 키보드 명령을 하면 스마트 자동차가 움직이는 예제.
 *  
 *  명령
 *  1. 터미널에 키보드로 g 라고 입력함
 *  -> 로봇이 전진
 *  2. 터미널에 키보드로 b 라고 입력함
 *  -> 로봇이 후진
 *  3. 터미널에 키보드로 s 라고 입력함
 *  -> 로봇이 정지
 *  
 */
int prev_speed = 0;

int RightMotor_E_pin = 5;      // 오른쪽 모터의 Enable & PWM
int RightMotor_1_pin = 8;      // 오른쪽 모터 제어선 IN1
int RightMotor_2_pin = 9;     // 오른쪽 모터 제어선 IN2
int LeftMotor_3_pin = 10;      // 왼쪽 모터 제어선 IN3
int LeftMotor_4_pin = 11;      // 왼쪽 모터 제어선 IN4
int LeftMotor_E_pin = 6;      // 왼쪽 모터의 Enable & PWM

// 명령 함수들
void SmartCar_Go();
void SmartCar_Back();
void SmartCar_Stop();

char prev_command;
int E_carSpeed = 153; // 최대 속도의  60 % 


void setup() {
  // declare the ledPin as an OUTPUT:
  pinMode(RightMotor_E_pin, OUTPUT);        // 출력모드로 설정
  pinMode(RightMotor_1_pin, OUTPUT);
  pinMode(RightMotor_2_pin, OUTPUT);
  pinMode(LeftMotor_3_pin, OUTPUT);
  pinMode(LeftMotor_4_pin, OUTPUT);
  pinMode(LeftMotor_E_pin, OUTPUT);

  Serial.begin(9600);                       // PC와의 시리얼 통신 9600bps로 설정

  Serial.println("Welcome Eduino!");

  digitalWrite(RightMotor_E_pin, HIGH);     // 오른쪽 모터의 Enable
  digitalWrite(LeftMotor_E_pin, HIGH);      // 왼쪽 모터의 Enable
}

void loop() {
  if (Serial.available())   // PC와의 시리얼통신으로 부터 받은 값이 있는지 판단
  {
    char command = Serial.read();    // 명령 저장
    Serial.println("Recived command");
    if(command == 'g'){               // 전진 명령
      SmartCar_Go();
    }
    else if(command == 'b'){          // 후진 명령
      SmartCar_Back();
    }
    else if(command == 's'){          // 정지 명령
      SmartCar_Stop();
    }
    else if(command == 'l'){          // 우회전 명령
      SmartCar_Right();
      
    }
    else if(command == 'r'){          // 좌회전 명령
      SmartCar_Left();
    }
    else{      
    }
  }
}

void SmartCar_Go(){        // 전진
    Serial.println("Forward");
    digitalWrite(RightMotor_1_pin, LOW);    
    digitalWrite(RightMotor_2_pin, HIGH);
    digitalWrite(LeftMotor_3_pin, LOW);    
    digitalWrite(LeftMotor_4_pin, HIGH);

    for(int i=0; i<=E_carSpeed; i=i+5){
      analogWrite(RightMotor_E_pin, i);     // 오른쪽 모터 전진 PWM제어
      analogWrite(LeftMotor_E_pin, i);
      delay(20); 
   }    
   prev_command = 'g';
}
void SmartCar_Back(){        // 후진
    Serial.println("Backward");
    digitalWrite(RightMotor_1_pin, HIGH);    
    digitalWrite(RightMotor_2_pin, LOW);
    digitalWrite(LeftMotor_3_pin, HIGH);    
    digitalWrite(LeftMotor_4_pin, LOW);

    for(int i=0; i<=E_carSpeed; i=i+5){
      analogWrite(RightMotor_E_pin, i);     // 오른쪽 모터 전진 PWM제어
      analogWrite(LeftMotor_E_pin, i);
      delay(20); 
    }    
    prev_command = 'b';
}
void SmartCar_Stop(){       // 정지
    for(int i=E_carSpeed; i>=0; i=i-5){
      if(prev_command == 'g'){
        analogWrite(RightMotor_E_pin, i);  
        analogWrite(LeftMotor_E_pin, i);
        delay(20); 
      }else if(prev_command == 'b'){
        analogWrite(RightMotor_E_pin, i);  
        analogWrite(LeftMotor_E_pin, i);
        delay(20); 
      }
    }   
    digitalWrite(RightMotor_E_pin, LOW);  // 오른쪽 모터 정지
    digitalWrite(LeftMotor_E_pin, LOW);   // 왼쪽 모터 정지
}

void SmartCar_Left()  // 좌회전
{
  digitalWrite(RightMotor_1_pin, LOW);    
  digitalWrite(RightMotor_2_pin, HIGH);
  digitalWrite(LeftMotor_3_pin, LOW);    
  digitalWrite(LeftMotor_4_pin, HIGH);
  prev_speed = 0;
  //Serial.println("leftleft");

  for (int i = prev_speed; i <= E_carSpeed; i = i + 5) {
    analogWrite(RightMotor_E_pin, i * 1.4);           // 140%
    analogWrite(LeftMotor_E_pin, i * 0.1);            // 20%
    delay(50);
  }
  prev_speed = E_carSpeed;
  delay(300);
  analogWrite(RightMotor_E_pin, prev_speed);
  analogWrite(LeftMotor_E_pin, prev_speed);
  
}
void SmartCar_Right() // 우회전
{
  digitalWrite(RightMotor_1_pin, LOW);    
  digitalWrite(RightMotor_2_pin, HIGH);
  digitalWrite(LeftMotor_3_pin, LOW);    
  digitalWrite(LeftMotor_4_pin, HIGH);
  
  prev_speed = 0;
  for (int i = prev_speed; i <= E_carSpeed; i = i + 5) {
    analogWrite(RightMotor_E_pin, i * 0.1);           // 20%
    analogWrite(LeftMotor_E_pin, i * 1.4);            // 140%
    delay(50);
  }
  prev_speed = E_carSpeed;
  delay(300);
  analogWrite(RightMotor_E_pin, prev_speed);
  analogWrite(LeftMotor_E_pin, prev_speed);
}
