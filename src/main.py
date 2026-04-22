# -*- coding: utf-8 -*-
import cv2
from ultralytics import YOLO
import serial
import time

# YOLOv8 모델 로드
model = YOLO('/home/mina/Downloads/best.pt')

# 시리얼 포트 설정
arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)

# 카메라 캡처 시작
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

def capture_frame():
    ret, frame = cap.read()
    if not ret:
        print("프레임을 가져올 수 없습니다.")
        return None
    return frame

def detect_objects(frame):
    results = model(frame)[0].boxes
    return results

# 상태 변수들
can_send_signal = True  # 아두이노 신호 수신 여부 플래그
previous_results = []  # 이전 프레임 감지 결과 저장
had_objects = False    # 이전 프레임에서 객체가 있었는지 확인하는 플래그
no_object_confirmed = False  # 객체가 없는 상태가 확인되었는지

while True:
    # 현재 프레임 캡처
    current_frame = capture_frame()
    if current_frame is None:
        continue

    # 현재 프레임 감지
    current_results = detect_objects(current_frame)
    
    # 현재 프레임에 객체가 있는지 확인
    has_objects = len(current_results) > 0
    
    # 객체 상태 변화 감지 로직
    if has_objects:  # 현재 객체가 있음
        if not had_objects and can_send_signal:  # 이전에 객체가 없었고, 신호를 보낼 수 있는 상태
            print("객체가 새로 감지되었습니다!")
            for result in current_results:
                class_id = int(result.cls)
                arduino.write("{}\n".format(class_id).encode())
                print(f"아두이노로 신호 전송: 클래스 ID {class_id}")
            can_send_signal = False
            no_object_confirmed = False
        
        # 객체가 있는 상태에서의 변화 감지
        if len(current_results) == len(previous_results) and len(previous_results) > 0:
            significant_change = False
            for i in range(len(current_results)):
                try:
                    # 현재 결과의 좌표 및 클래스 정보
                    c_xmin, c_ymin, c_xmax, c_ymax = current_results[i].xyxy[0].cpu().numpy()
                    c_cls = int(current_results[i].cls.cpu().numpy())
                    
                    # 이전 결과의 좌표 및 클래스 정보
                    p_xmin, p_ymin, p_xmax, p_ymax = previous_results[i].xyxy[0].cpu().numpy()
                    p_cls = int(previous_results[i].cls.cpu().numpy())
                    
                    if model.names[p_cls] == model.names[c_cls]:
                        # 좌표 변화 계산
                        diff_xmin = abs(c_xmin - p_xmin)
                        diff_ymin = abs(c_ymin - p_ymin)
                        diff_xmax = abs(c_xmax - p_xmax)
                        diff_ymax = abs(c_ymax - p_ymax)
                        
                        if not (diff_xmin <= 20 and diff_ymin <= 20 and 
                               diff_xmax <= 20 and diff_ymax <= 20):
                            significant_change = True
                except Exception as e:
                    print(f"좌표 비교 중 오류 발생: {str(e)}")
                    significant_change = True
                    
            if significant_change and can_send_signal:
                for result in current_results:
                    class_id = int(result.cls)
                    arduino.write("{}\n".format(class_id).encode())
                    print(f"객체 위치 변화로 인한 신호 전송: 클래스 ID {class_id}")
                can_send_signal = False
        
        had_objects = True
        
    else:  # 현재 객체가 없음
        if had_objects and not no_object_confirmed:  # 이전에 객체가 있었고, 아직 확인되지 않은 경우
            print("객체가 사라졌습니다!")
            no_object_confirmed = True
            had_objects = False
            can_send_signal = True  # 다음 객체 감지를 위해 신호 전송 가능 상태로 변경
    
    # 아두이노로부터 완료 신호 수신 대기
    if arduino.in_waiting > 0:
        response = arduino.readline().decode().strip()
        print(f"아두이노로부터 수신한 신호: {response}")
        if response == "1":  # 모터 동작 완료 신호 수신
            can_send_signal = True
            print("아두이노 모터 동작 완료 - 신호 전송 가능 상태로 변경")
    
    # 결과 시각화
    annotated_frame = model(current_frame)[0].plot()
    cv2.imshow('YOLOv8 Detection', annotated_frame)
    
    # ESC로 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break
    
    previous_results = current_results

# 자원 해제
cap.release()
cv2.destroyAllWindows()
arduino.close()
