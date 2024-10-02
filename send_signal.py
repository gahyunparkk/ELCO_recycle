import cv2
from ultralytics import YOLO
import serial
import time

# YOLOv8 모델 로드
model = YOLO('C:/Users/gahyu/Downloads/runs/runs/detect/yolov8_cuton_model/weights/best.pt')

# 시리얼 포트 설정 (아두이노 포트에 맞게 수정)
arduino = serial.Serial('COM10', 9600)
time.sleep(2)  # 시리얼 통신 안정화를 위해 잠시 대기

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
    results = model(frame)[0].boxes  # 모델로 감지 수행
    return results

previous_results = []

while True:
    previous_frame = capture_frame()  # 이전 프레임 캡처
    previous_results = detect_objects(previous_frame)  # 이전 프레임 감지
    time.sleep(0.5)  # 0.5초 대기

    current_frame = capture_frame()  # 현재 프레임 캡처
    current_results = detect_objects(current_frame)  # 현재 프레임 감지

    # 이전 및 현재 프레임에서 감지된 객체 비교
    if len(current_results) == len(previous_results):
        significant_change = False
        
        # 좌표 비교
        for i in range(len(current_results)):
            # 이전 결과의 좌표 및 클래스 정보
            p_xmin, p_ymin, p_xmax, p_ymax = previous_results[i].xyxy[0].cpu().numpy()
            p_cls = int(previous_results[i].cls.cpu().numpy())

            # 현재 결과의 좌표 및 클래스 정보
            c_xmin, c_ymin, c_xmax, c_ymax = current_results[i].xyxy[0].cpu().numpy()
            c_cls = int(current_results[i].cls.cpu().numpy())

            if model.names[p_cls] == model.names[c_cls]:  # 클래스가 같은 경우
                # 좌표 변화 계산
                diff_xmin = abs(c_xmin - p_xmin)
                diff_ymin = abs(c_ymin - p_ymin)
                diff_xmax = abs(c_xmax - p_xmax)
                diff_ymax = abs(c_ymax - p_ymax)

                # 모든 변화가 20 이하인지 확인
                if not (diff_xmin <= 20 and diff_ymin <= 20 and diff_xmax <= 20 and diff_ymax <= 20):
                    significant_change = True

        # 변화가 없으면 아두이노로 신호 전송
        if not significant_change:
            for result in current_results:
                class_id = int(result.cls)  # 클래스 ID 추출
                arduino.write(f"{class_id}\n".encode())  # 클래스 ID 전송

    # 결과 프레임에 감지된 객체들을 시각화
    annotated_frame = model(current_frame)[0].plot()
    cv2.imshow('YOLOv8 Detection', annotated_frame)

    # ESC를 눌러 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
arduino.close()  # 아두이노 시리얼 포트 닫기
