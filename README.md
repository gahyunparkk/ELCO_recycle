# ♻️ 딥러닝을 이용한 분리수거 자동화 머신
> **YOLOv8과 Arduino를 활용한 실시간 쓰레기 분류 및 자동 배출 시스템**
> 
> **국민대학교 전자공학부 소모임 ELCO 2024 전시회**

본 프로젝트는 주변에서 분리수거가 제대로 이루어지지 않는 문제를 해결하기 위해 기획되었습니다. 딥러닝 기반의 객체 인식 기술(YOLOv8)과 하드웨어 제어(Arduino)를 결합하여, 쓰레기를 자동으로 분류하고 알맞은 곳으로 배출해주는 스마트 머신을 개발했습니다.

---

## 🛠 Tech Stack

### **Environment**
| Category | Details |
| :--- | :--- |
| **OS** | Ubuntu 20.04 (Training) / Windows 10, 11 (Inference) |
| **Language** | Python 3.10.11 |
| **AI Framework** | YOLOv8n, PyTorch 2.2.0 (**CUDA 11.8**) |
| **IDE/Tool** | Arduino IDE, VS Code |

### **Hardware**
* **Controller:** Arduino Uno
* **Actuator:** Servo Motor x3, LED
* **Sensor:** Logitech Webcam

---

## 🏗 System Architecture

본 시스템은 웹캠을 통해 들어오는 영상 데이터를 실시간으로 분석하여 물리적인 분류까지 이어지는 통합 파이프라인으로 구성되어 있습니다.

1.  **Data Capture:** 웹캠을 통해 쓰레기 이미지를 실시간으로 입력받습니다.
2.  **Object Detection (YOLOv8):** 학습된 모델이 쓰레기의 종류를 4가지 클래스(캔, 종이, 플라스틱, 유리)로 분류합니다.
3.  **Stability Logic (Decision):** 객체의 Class와 Bounding Box 좌표가 0.5초 동안 안정적으로 유지될 경우에만 실제 물체가 투입된 것으로 판단하여 신뢰성을 확보했습니다.
4.  **Signal Processing:** 판단된 정보를 Serial 통신을 통해 아두이노로 전송합니다.
5.  **Hardware Control:** 아두이노는 수신된 클래스 정보에 따라 3개의 서보 모터를 구동하여 쓰레기를 알맞은 투입구로 분류합니다.

---

## 📂 Directory Structure

```
├── arduino/
│   └── svo.ino              # 아두이노 모터 제어 및 핸드셰이크 통신 코드
├── model/
│   └── yolo_train.py        # YOLOv8 모델 학습 스크립트 (Linux 환경)
├── src/
│   ├── main.py              # [Main] 실시간 인식 및 통신 통합 코드 (Windows 환경)
│   └── old_version/
│       └── v1_detection.py 
├── tests/
│   └── keyboard_input_to_arduino.py  # 하드웨어 동작 수동 테스트 코드
├── README.md
└── requirements.txt         # 필수 라이브러리 목록
```

---

## 🚀 Getting Started

### 1. Environment Setup
본 프로젝트는 CUDA 11.8 환경에 최적화되어 있습니다. 아래 명령어를 통해 필수 라이브러리를 설치합니다.

```
# 1. CUDA 11.8에 맞는 PyTorch 설치 (Windows/Linux 공통)
pip install torch==2.2.0 torchvision --index-url https://download.pytorch.org/whl/cu118

# 2. 기타 필수 라이브러리 설치
pip install -r requirements.txt
```

### 2. How to Run
1. `arduino/svo.ino` 파일을 아두이노 우노에 업로드합니다.
2. 사용 중인 운영체제에 맞춰 `src/main.py`의 시리얼 포트 설정을 확인합니다. (Windows: COM*, Linux: `/dev/tty*`)
3. `python src/main.py`를 실행하여 시스템을 가동합니다.

---

## 📊 Model Training & Dataset

실생활에서 높은 인식 정확도를 확보하기 위해 대규모 공공 데이터셋과 직접 구축한 커스텀 데이터셋을 혼합하여 학습을 진행했습니다.

* **Classes:** 4종 (Can, Paper, Plastic, Glass)
* **Dataset Composition:**
    * **AI Hub [생활 폐기물 이미지](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=140):** * 약 100,000장의 데이터 활용
        * 유리병, 종이류, 캔류, 페트병, 플라스틱류 카테고리를 선별하여 다운로드 후 전처리 진행
        * 페트병과 플라스틱류는 특징의 유사성을 고려하여 '플라스틱' 클래스로 통합 학습
    * **Custom Dataset:** 직접 촬영 및 크롤링 데이터 약 500장 (직접 라벨링 수행)
* **Hyperparameters:**
    * **Input Size:** $640 \times 640$
    * **Batch Size:** 16
    * **Epoch:** 100
    * **Optimizer:** AdamW (Learning Rate: 0.001)
<img width="2400" height="1200" alt="Image" src="https://github.com/user-attachments/assets/c34deab1-c5e8-458e-b7d3-a2466c7df52a" />
---

## 📚 References
* [AI Hub 생활 폐기물 이미지 데이터셋](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=140)
* [Ultralytics YOLOv8 Documentation](https://docs.ultralytics.com/)
* 국민대학교 전자공학부 학술소모임 ELCO
