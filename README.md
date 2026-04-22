# ♻️ 딥러닝을 이용한 분리수거 자동화 머신
> **YOLOv8과 Arduino를 활용한 실시간 쓰레기 분류 및 자동 배출 시스템**
> 
> **국민대학교 전자공학부 소모임 ELCO 2024 전시회**

본 프로젝트는 주변에서 분리수거가 제대로 이루어지지 않는 문제를 해결하기 위해 기획되었습니다. 딥러닝 기반의 객체 인식 기술(YOLOv8)과 하드웨어 제어(Arduino)를 결합하여, 쓰레기를 자동으로 분류하고 알맞은 곳으로 배출해주는 스마트 머신을 개발했습니다.
국민대학교 전자공학부 소모임 ELCO 2024 전시회

---

## 🛠 Tech Stack

### **Hardware**
* **Controller:** Arduino Uno
* **Actuator:** Servo Motor, LED
* **Sensor:** Logitech Webcam

### **Software & AI**
* **OS:** Ubuntu 20.04 (Linux), Windows
* **Language:** Python 3.10.11
* **Model:** YOLOv8n
* **Library/Tool:**
    * PyTorch 2.2.0
    * **CUDA 11.8**
    * Ultralytics
    * Arduino IDE (Serial Communication)

---

## 🏗 System Architecture

본 시스템은 웹캠을 통해 들어오는 영상 데이터를 실시간으로 분석하여 물리적인 분류까지 이어지는 통합 파이프라인으로 구성되어 있습니다.

1.  **Data Capture:** 웹캠을 통해 쓰레기 이미지를 실시간으로 입력받습니다.
2.  **Object Detection (YOLOv8):** 학습된 모델이 쓰레기의 종류를 4가지 클래스로 분류합니다.
3.  **Stability Logic (Decision):** 객체의 Class와 Bounding Box 좌표가 **0.5초 동안 안정적으로 유지**될 경우, 실제 물체가 인식된 것으로 판단합니다.
4.  **Signal Processing:** 판단된 정보를 Serial 통신을 통해 아두이노로 전송합니다.
5.  **Hardware Control:** 아두이노는 수신된 클래스 정보에 따라 서보 모터를 구동하여 쓰레기를 알맞은 투입구로 분류합니다.

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

---

## 🌟 Key Responsibilities (Leadership)

본 프로젝트는 국민대학교 전자공학부 학술소모임 **ELCO** 2024 전시회 출품작으로, 저는 **팀장**으로서 기술적 구현과 팀 협업을 주도했습니다.

* **Model Engineering:** AI Hub의 대규모 데이터를 필터링하고 커스텀 데이터와 결합하는 데이터 전략 수립 및 YOLOv8 모델 학습 총괄.
* **Leadership & Mentoring:** 1학년 신입 부원 및 멘티들이 프로젝트에 기여할 수 있도록 정기적인 **코드 리뷰**를 진행하고, 딥러닝 라이브러리 설치 및 환경 구성을 지원함.
* **Troubleshooting:** 실시간 영상 분석 시 발생하는 미세한 흔들림으로 인한 시리얼 통신 과부하 문제를 해결하기 위해, **'0.5초 유지 시 전송'**하는 데이터 버퍼링 로직을 설계하여 시스템 안정성 확보.

---

## ⚠️ Important Note
* 본 리포지토리의 아두이노 코드는 `Arduino Uno`와 서보 모터 회로 구성이 필요합니다.
* Python 환경 구동 시 `requirements.txt`에 명시된 PyTorch 및 CUDA 11.8 환경을 권장합니다.

---

## 📚 References
* [AI Hub 생활 폐기물 이미지 데이터셋](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=140)
* [Ultralytics YOLOv8 Documentation](https://docs.ultralytics.com/)
* 국민대학교 전자공학부 학술소모임 ELCO
