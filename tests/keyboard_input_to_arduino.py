import serial
import time

# 시리얼 포트 설정 (아두이노 포트에 맞게 수정)
arduino = serial.Serial('COM4', 9600)
time.sleep(2)  # 시리얼 통신 안정화를 위해 잠시 대기

can_send_signal = True  # 아두이노 신호 수신 여부 플래그

while True:
    if can_send_signal:
        # 사용자 입력으로 클래스 ID 입력받기 (0, 1, 2, 3 중 하나)
        try:
            class_id = int(input("아두이노로 보낼 클래스 ID (0, 1, 2, 3): "))
            if class_id not in [0, 1, 2, 3]:
                print("0, 1, 2, 3 중 하나를 입력하세요.")
                continue
        except ValueError:
            print("숫자를 입력하세요.")
            continue

        # 아두이노로 신호 전송
        arduino.write(f"{class_id}\n".encode())
        print(f"아두이노로 신호 전송: 클래스 ID {class_id}")
        can_send_signal = False  # 신호 전송 후 대기 상태로 변경

    # 아두이노로부터 완료 신호 수신 대기
    if arduino.in_waiting > 0:
        response = arduino.readline().decode().strip()
        print(f"아두이노로부터 수신한 신호: {response}")
        if response == "1":  # 모터 동작 완료 신호 수신
            can_send_signal = True  # 신호 전송 가능 상태로 변경
            print("아두이노 모터 동작 완료 신호 수신 - 신호 전송 가능 상태로 변경")

# 자원 해제
arduino.close()  # 아두이노 시리얼 포트 닫기
