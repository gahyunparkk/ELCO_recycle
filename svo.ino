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
  Serial.println("서보모터 제어 시작. 1, 2, 3, 4를 입력하세요.");

  // 1번 모터의 초기값을 90도로 설정
   // 1번 모터를 90도 위치로 이동
  Serial.println("1번 모터 초깃값: 90도");
}

void loop() {
  motor1.write(90);
  motor2.write(90);
  motor3.write(90);

  if (Serial.available() > 0) {  // 입력 값이 있을 때만 동작
    int input = Serial.parseInt();

    // 입력 값에 따라 서보모터 제어
    switch (input) {
      case 0:
        motor1.write(135);  // 1번 모터를 45도 회전
        Serial.println("1번 모터: 45도");
        delay(5000);       // 1초 대기
        motor1.write(90);  // 1번 모터를 다시 90도로 원상복구
        Serial.println("1번 모터: 90도로 복귀");
        break;

      case 1:
        motor1.write(180);  // 1번 모터는 이미 90도 상태 유지
        motor2.write(45);  // 2번 모터를 45도 회전
        Serial.println("1번 모터: 90도, 2번 모터: 45도");
        delay(5000);       // 1초 대기
        motor1.write(90);
        motor2.write(90);   // 2번 모터 원상복구 (0도)
        Serial.println("2번 모터 원상복구 (0도)");
        break;

      case 2:
        motor1.write(180);  // 1번 모터는 90도 유지
        motor2.write(90);   // 2번 모터를 0도 회전
        motor3.write(45);  // 3번 모터를 45도 회전
        Serial.println("1번 모터: 90도, 2번 모터: 0도, 3번 모터: 45도");
        delay(2000);       // 1초 대기
        motor1.write(90);
        motor2.write(90);   // 2번 모터는 0도로 유지
        motor3.write(90);   // 3번 모터 원상복구 (0도)
        Serial.println("2번, 3번 모터 원상복구 (0도)");
        break;

      case 3:
        motor1.write(180);  // 1번 모터는 이미 90도 유지
        motor2.write(90);   // 2번 모터를 0도 유지
        motor3.write(90);   // 3번 모터를 0도로 유지
        Serial.println("1번 모터: 90도, 2번 모터: 0도, 3번 모터: 0도");
        delay(5000);       // 1초 대기
        motor1.write(90);
        motor2.write(90);   // 2번 모터는 0도로 유지
        motor3.write(90);   // 3번 모터는 0도로 유지
        Serial.println("2번, 3번 모터 원상복구 (0도)");
        break;

      default:
        break;
    }

    // 모터가 원상복구되는 시간을 기다림
    delay(3000);
  }
}
