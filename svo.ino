#include <Servo.h>

Servo motor1;  // 1번 모터
Servo motor2;  // 2번 모터
Servo motor3;  // 3번 모터

void setup() {
  motor1.attach(9);   // 1번 모터를 9번 핀에 연결
  motor2.attach(10);  // 2번 모터를 10번 핀에 연결
  motor3.attach(11);  // 3번 모터를 11번 핀에 연결
  
  Serial.begin(9600);  // 시리얼 통신 시작
  
  motor1.write(90);  // 초기 위치 설정
  motor2.write(90);
  motor3.write(90);
}

void loop() {
  if (Serial.available() > 0) {  // 입력 값이 있을 때만 동작
    int input = Serial.parseInt();

    switch (input) {
      case 0:
        motor1.write(135);  
        delay(5000);       
        motor1.write(90);  
        break;

      case 1:
        motor1.write(180);  
        motor2.write(45);  // 2번 모터를 45도 회전
        delay(5000);       
        motor1.write(90);
        motor2.write(90);   // 2번 모터 원상복구 (0도)
        break;

      case 2:
        motor1.write(180); 
        motor2.write(90);   // 2번 모터를 0도 회전
        motor3.write(45);  // 3번 모터를 45도 회전
        delay(2000);       
        motor1.write(90);
        motor2.write(90);   // 2번 모터는 0도로 유지
        motor3.write(90);   // 3번 모터 원상복구 (0도)
        break;

      case 3:
        motor1.write(180); 
        motor2.write(90);   // 2번 모터를 0도 유지
        motor3.write(90);   // 3번 모터를 0도로 유지 
        delay(5000);       
        motor1.write(90);
        motor2.write(90);   // 2번 모터는 0도로 유지
        motor3.write(90);   // 3번 모터는 0도로 유지
        break;

      default:
        Serial.println("잘못된 입력입니다.");
        break;
    }

    delay(3000);  // 모터가 원상복구되는 시간을 기다림
    Serial.println("1");  // 파이썬에 모터 동작 완료 신호 전송

    // 버퍼에 남아 있는 데이터를 제거하여 다음 명령에서 불필요한 반복을 방지
    while (Serial.available() > 0) {
      Serial.read();
    }
  }
}
