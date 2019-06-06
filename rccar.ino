/*Real
Real
*/
//핀 설정 
const int EnablePinRight = 7;     //오른쪽 모터 Enable 핀 
const int StepPinRight = 6;       //오른쪽 모터 PWM 핀 
const int DirectionPinRight = 5;  //오른쪽 모터 방향 핀 
const int EnablePinLeft = 4;      //왼쪽 모터 Enable 핀 
const int StepPinLeft = 3;        //왼쪽 모터 PWM 핀 
const int DirectionPinLeft = 2;   //왼쪽 모터 방향 핀 
//속도 
const int FastMove = 200;
const int SlowMove = 600;
const int SlowSlowMove = 1700;    //좌,우회전시 딜레이
//초음파
const int pwPin1 = 10;
const int pwPin2 = 9;
long sensor1, sensor2, sensorreal;

void SmartCar_Go();
void SmartCar_Back();
void SmartCar_Stop();
void SmartCar_Left();
void SmartCar_Right();
void read_sensor();
void printsensor();
void smallersensor();
char prev_command = 's';          //초기 명령 정지 설정
char command;

void setup() 
{
  // 핀 설정 
  pinMode(EnablePinLeft, OUTPUT);
  pinMode(StepPinLeft, OUTPUT); 
  pinMode(DirectionPinLeft, OUTPUT);
  pinMode(EnablePinRight, OUTPUT);
  pinMode(StepPinRight, OUTPUT); 
  pinMode(DirectionPinRight, OUTPUT);
  pinMode(pwPin1, INPUT);
  pinMode(pwPin2, INPUT);
  digitalWrite(DirectionPinLeft,HIGH); //High 상태는 시계방향 이동
  digitalWrite(DirectionPinRight,LOW); //Low 상태는 반시계방향 이동

  Serial.begin(9600);
  // 모터 IC ON
  digitalWrite(EnablePinLeft,LOW);
  digitalWrite(EnablePinRight,LOW); 
}

void smallersensor(){
  //초음파센서값 두 개 중에서 작은 값
  /*
  if(sensor1>sensor2){
    sensorreal = sensor2;
  }
  else{
    sensorreal = sensor1;
  }
  */
  sensorreal = sensor2;
}

void printsensor(){         
  Serial.println(sensorreal);      //라즈베리파이에게 초음파센서값 전송
}

void read_sensor(){
  //sensor1 = pulseIn(pwPin1, HIGH); //
  sensor2 = pulseIn(pwPin2, HIGH);
}

void loop() {
  read_sensor();
  smallersensor();
  printsensor();
  
  if(Serial.available()){
    command = Serial.read();     //명령 저장
  } 
  else if (prev_command == 'r' || prev_command == 'l'){
    command = 'g';               //우회전,좌회전 후에 전진
  } 
  else {
    command = prev_command;
  }
  if(command == 'g'){            // 전진 명령
    SmartCar_Go();
  }
  
  else if(command == 's'){       // 정지 명령
    SmartCar_Stop();
  }
  else if(command == 'l'){       // 좌회전 명령
    SmartCar_Left();
  }
  else if(command == 'r'){       // 우회전 명령
    SmartCar_Right();
  }
  else{      
  } 
}
/* cheapest 초음파
void Distance_Measurement() {
  digitalWrite(triggerPin, LOW);
  delay(2);
  digitalWrite(triggerPin, HIGH);  // trigPin에서 초음파 발생(echoPin도 HIGH)
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  duration = pulseIn(echoPin, HIGH);    // echoPin 이 HIGH를 유지한 시간을 저장 한다.
  distance = ((float)(340 * duration) / 1000) / 2;
  delay(1000);
  Serial.println(distance);
  Serial.println("distance");
  prev_command = 'd';
}
*/
/*
 * A4988
 * ms1, ms3 : high
 * ms2 : low
 * step핀이 4번 움직이면 1.8도 이동하게 됨.
 */
void SmartCar_Go () {     // 전진
  digitalWrite(DirectionPinLeft,HIGH); //High 상태는 시계방향 이동
  digitalWrite(DirectionPinRight,LOW);
  if (prev_command == 's' || prev_command == 'l' || prev_command =='r'){
    //Serial.println(prev_command);
    for(int i = 1600; i > SlowMove ; i--) //점점 빨라지며 전진시작
    {
    digitalWrite(StepPinLeft,HIGH);//ON 1.8의 1/4 움직임
    digitalWrite(StepPinRight,HIGH);
    delayMicroseconds(i);//ims 대기   
    digitalWrite(StepPinLeft,LOW);//OFF 1.8의 1/4 움직임
    digitalWrite(StepPinRight,LOW);
    delayMicroseconds(i);//ims 대기
    if (sensorreal < 600) {
      digitalWrite(StepPinLeft,LOW);
      digitalWrite(StepPinRight,LOW);
      prev_command = 's';
      return;
    }
    }
  for(int i = 0; i < 800; i++)  //2400/8=3바퀴 직진
  {
    digitalWrite(StepPinLeft,HIGH); //ON 1.8의 1/4 움직임
    digitalWrite(StepPinRight,HIGH);
    delayMicroseconds(SlowMove);    //600ms 대기   
    digitalWrite(StepPinLeft,LOW);  //OFF 1.8의 1/4 움직임
    digitalWrite(StepPinRight,LOW);
    delayMicroseconds(SlowMove);    //600ms 대기
    if (sensorreal < 600) {
      digitalWrite(StepPinLeft,LOW);
      digitalWrite(StepPinRight,LOW);
      prev_command = 's';
      return;
     
    }
  }
  }
  else{
    for(int i = 0; i < 1600; i++)  //3바퀴 직진
    {
      digitalWrite(StepPinLeft,HIGH);   //ON 1.8의 1/4 움직임
      digitalWrite(StepPinRight,HIGH);
      delayMicroseconds(SlowMove);      //600ms 대기   
      digitalWrite(StepPinLeft,LOW);    //OFF 1.8의 1/4 움직임
      digitalWrite(StepPinRight,LOW);
      delayMicroseconds(SlowMove);      //600ms 대기
      if (sensorreal < 600) {           //초음파센서 값이 450mm 미만이면
        digitalWrite(StepPinLeft,LOW);
        digitalWrite(StepPinRight,LOW); //정지
        prev_command = 's';
        return;
      }
    }
  }
  prev_command = 'g';
}




/*
void SmartCar_Back(){        // 후진
 // if (prev_command == 'b') {
 //     return;
 // }
  digitalWrite(DirectionPinLeft,LOW); //High 상태는 시계방향 이동
  digitalWrite(DirectionPinRight,HIGH);
  for(int i = 0; i < 2000; i++)
  {
    digitalWrite(StepPinLeft,HIGH);//OFF 1.8의 1/4 움직임
    digitalWrite(StepPinRight,HIGH);     
    delayMicroseconds(FastMove);
    digitalWrite(StepPinLeft,LOW);//OFF 1.8의 1/4 움직임
    digitalWrite(StepPinRight,LOW);
    delayMicroseconds(SlowSlowMove);
  }
  prev_command = 'b';
}
*/

void SmartCar_Stop(){       // 정지
  if(prev_command == 'g'){
    

  digitalWrite(StepPinLeft,LOW);
  digitalWrite(StepPinRight,LOW);
  prev_command = 's';  
  }

  /*for(int i = 600; i <= 1000; i++)
  {
      //ON 1.8의 1/4 움직임
      digitalWrite(StepPinLeft,HIGH);
      digitalWrite(StepPinRight,HIGH);
      //1ms(1000us) 대기     
      delayMicroseconds(i);
      //OFF 1.8의 1/4 움직임
      digitalWrite(StepPinLeft,LOW);
      digitalWrite(StepPinRight,LOW);
      //1ms(1000us) 대기
      delayMicroseconds(i);
    }
    digitalWrite(StepPinLeft,LOW);
    digitalWrite(StepPinRight,LOW);
  }
  else{
    digitalWrite(StepPinLeft,LOW);
    digitalWrite(StepPinRight,LOW);
  }*/
    /*
    else if(prev_command == 'b'){
      //ON 1.8의 1/4 움직임
      digitalWrite(StepPinLeft,HIGH);
      digitalWrite(StepPinRight,HIGH);
      //1ms(1000us) 대기     
      delayMicroseconds(i);
      //OFF 1.8의 1/4 움직임
      digitalWrite(StepPinLeft,LOW);
      digitalWrite(StepPinRight,LOW);
      //1ms(1000us) 대기
      delayMicroseconds(i);
    }
  }*/

}

void SmartCar_Left()  // 좌회전
{   
 
  for(int i = 0; i < 800; i++)       //왼쪽으로 한 바퀴 회전
  {
    digitalWrite(StepPinLeft,HIGH);
    digitalWrite(StepPinRight,HIGH);
    delayMicroseconds(FastMove);     //200ms 대기
    digitalWrite(StepPinRight,LOW);
    delayMicroseconds(SlowSlowMove); //1700ms 대기
    digitalWrite(StepPinLeft,LOW);
    digitalWrite(StepPinRight,HIGH);
    delayMicroseconds(FastMove);     //600ms 대기
    digitalWrite(StepPinRight,LOW);
    delayMicroseconds(SlowSlowMove); //1700ms 대기
  }
  prev_command = 'l';
}

void SmartCar_Right()  // 우회전
{   
  for(int i = 0; i < 800; i++)       //오른쪽으로 한 바퀴 회전
  {
    digitalWrite(StepPinLeft,HIGH);
    digitalWrite(StepPinRight,HIGH);
    delayMicroseconds(FastMove);     //200ms 대기
    digitalWrite(StepPinLeft,LOW);
    delayMicroseconds(SlowSlowMove); //1700ms 대기
    digitalWrite(StepPinLeft,HIGH);
    digitalWrite(StepPinRight,LOW);
    delayMicroseconds(FastMove);     //200ms 대기
    digitalWrite(StepPinLeft,LOW);
    delayMicroseconds(SlowSlowMove); //1700ms 대기
  }
  prev_command = 'r';
}
