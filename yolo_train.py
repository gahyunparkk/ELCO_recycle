from ultralytics import YOLO

# 모델 초기화
model = YOLO('yolov8n.pt')

# 학습 설정
model.train(
    data='data.yaml',  # 데이터 설정 파일 경로
    epochs=100,                # 학습할 에포크 수
    imgsz=640,                 # 이미지 크기
    batch=16,                  # 배치 크기
    name='yolov8_cuton_model', # 결과를 저장할 폴더 이름
    lr0=0.001,                  # 초기 학습률 설정 (여기서는 0.001)
    verbose = True

)