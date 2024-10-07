#include <Servo.h>

Servo motor1;  // 1번 모터
Servo motor2;  // 2번 모터
Servo motor3;  // 3번 모터

void setup() {
  // 서보모터 핀 연결
  motor1.attach(9);   // 1번 모터를 9번 핀에 연결
  motor2.attach(10);  // 2번 모터를 10번 핀에 연결
  motor3.attach(11);  // 3번 모터를 11번 핀에 연결

  Serial.begin(9600);  // 시리얼 통신 시작
  Serial.println("서보모터 제어 시작. 0, 1, 2, 3을 입력하세요.");

  // 1번 모터의 초기값을 90도로 설정
  motor1.write(90);
  motor2.write(90);
  motor3.write(90);
}

void loop() {
  if (Serial.available() > 0) {  // 입력 값이 있을 때만 동작
    char input = Serial.read();  // 시리얼로 입력 받은 값 읽기

    // 공백 문자나 줄바꿈 문자는 무시
    
    // 입력 값에 따라 서보모터 제어
    if (input == '0') {
        // 모터 1이 90도에서 45도로 회전한 후 2초 후 다시 90도로 복귀
        motor1.write(135);  
        Serial.println("모터 1: 90도에서 45도로 회전");
        delay(2000);        // 2초 대기
        motor1.write(90);   // 다시 90도로 복귀
        Serial.println("모터 1: 다시 90도로 복귀");

    } else if (input == '1') {
        // 모터 1은 90도에서 45도로, 모터 2, 3은 0도 유지
        motor1.write(180);   // 1번 모터 45도
        motor2.write(45);    // 2번 모터 0도
        Serial.println("모터 1: 90도에서 45도, 모터 2: 0도, 모터 3: 0도");
        delay(2000);
        motor1.write(90);
        motor2.write(90);
        Serial.println("원상복구");

    } else if (input == '2') {
        // 모터 1은 90도에서 0도로, 모터 2는 0도에서 45도로, 모터 3은 0도 유지
        motor1.write(180);    // 1번 모터 0도
        motor3.write(45);    // 3번 모터 0도
        Serial.println("모터 1: 90도에서 0도, 모터 2: 0도에서 45도, 모터 3: 0도");
        delay(2000);
        motor1.write(90);
        motor3.write(90);
        Serial.println("원상복구");

    } else if (input == '3') {
        // 모터 1은 90도에서 0도로, 모터 2는 0도 유지, 모터 3은 0도에서 45도 회전
        motor1.write(180);    // 1번 모터 0도
        Serial.println("모터 1: 90도에서 0도, 모터 2: 0도, 모터 3: 0도에서 45도");
        delay(2000);
        motor1.write(90);
        Serial.println("원상복구");

    } else {
        Serial.println("잘못된 입력. 0, 1, 2, 3 중 하나를 입력하세요.");
    }

    // 모터가 움직인 후 1초 대기
    delay(1000);
    
    // "A"를 출력
    Serial.println("A");
  }
}
