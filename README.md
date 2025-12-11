# 📐 단위 변환 학습 웹앱

초등학교 3~4학년 수학 '도형과 측정' 영역 학습을 돕는 **단위 변환 연습** Streamlit 웹앱입니다.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)

---

## 📌 프로젝트 목적

학생들이 다음 단위 변환을 재미있게 연습할 수 있도록 설계되었습니다:
- **길이**: mm, cm, m, km
- **들이**: mL, L  
- **무게**: g, kg, t

---

## ✨ 주요 기능

### 1️⃣ **초기 화면 - 학습 영역 선택**
- 📏 **길이** 변환 학습
- 🥤 **들이** 변환 학습
- ⚖️ **무게** 변환 학습

### 2️⃣ **개념 설명 기능**
각 영역별 문제 화면에서 **"📘 개념 설명 보기"** 버튼으로 다음 내용을 확인할 수 있습니다:

**길이 영역:**
- mm, cm, m, km의 단위 관계
- 단위 변환 예시 및 실제 관계식
- 1 km = 1000 m = 100,000 cm = 1,000,000 mm

**들이 영역:**
- mL, L의 단위 관계  
- 1 L = 1000 mL
- 실생활 예시

**무게 영역:**
- g, kg, t의 단위 관계
- 1 kg = 1000 g, 1 t = 1000 kg
- 실생활 예시

### 3️⃣ **오답 시 힌트 기능 (v3.0 신규)**
오답일 경우 자동으로 "🔍 힌트 보기" expander가 나타납니다:
- **단위별 분석**: 틀린 단위만 자동으로 판별
- **맞춤형 힌트**: 해당 단위에 대한 구체적인 학습 가이드 제공
- **예시**:
  - cm이 틀렸다면: "1m = 100cm 관계를 다시 확인해보세요."
  - kg이 틀렸다면: "1kg = 1,000g, 1t = 1,000kg 관계를 다시 확인해보세요."

### 4️⃣ **길이 변환 문제**
```
문제 예: 10cm를 mm, cm, m, km으로 변환하세요
- 범위: 100mm ~ 100,000mm
- 정답이면: 새로운 난수 문제 자동 생성
- 오답이면: 메시지 + 힌트 표시
```

### 5️⃣ **들이 변환 문제**
```
문제 예: 1000mL을 mL, L로 변환하세요
- 범위: 10mL ~ 100,000mL
- 정답이면: 새로운 난수 문제 자동 생성
- 오답이면: 메시지 + 힌트 표시
```

### 6️⃣ **무게 변환 문제**
```
문제 예: 10kg을 g, kg, t로 변환하세요
- 범위: 10,000g ~ 1,000,000g
- 정답이면: 새로운 난수 문제 자동 생성
- 오답이면: 메시지 + 힌트 표시
```

### 7️⃣ **재시작 기능**
- 화면 하단의 "🔄 재시작" 버튼으로 초기 화면으로 돌아가기

---

## 🚀 실행 방법

### 1. 요구사항 설치
```bash
pip install -r requirements.txt
```

### 2. 앱 실행
```bash
streamlit run streamlit_app.py
```

### 3. 웹 브라우저에서 접속
```
http://localhost:8501
```

---

## 📁 프로젝트 구조

```
blank-app/
├── streamlit_app.py          # 메인 Streamlit 애플리케이션
├── utils/
│   ├── __init__.py           # 패키지 초기화
│   ├── converter.py          # 단위 변환 함수
│   └── generator.py          # 문제 생성 함수
├── requirements.txt          # 의존성 패키지 목록
├── README.md                 # 프로젝트 설명 (이 파일)
└── LICENSE                   # 라이선스
```

---

## 🛠 기술 스택

| 기술 | 버전 | 설명 |
|------|------|------|
| Python | 3.8+ | 프로그래밍 언어 |
| Streamlit | 1.28+ | 웹 애플리케이션 프레임워크 |

---

## 📊 코드 설명

### `converter.py` - 단위 변환 함수

#### `convert_length(value_mm)`
밀리미터를 모든 길이 단위로 변환합니다 (**Decimal 기반**).
```python
result = convert_length(Decimal('100'))
# {'mm': Decimal('100'), 'cm': Decimal('10'), 'm': Decimal('0.1'), 'km': Decimal('0.0001')}
```

#### `convert_capacity(value_ml)`
밀리리터를 모든 들이 단위로 변환합니다 (**Decimal 기반**).
```python
result = convert_capacity(Decimal('1000'))
# {'mL': Decimal('1000'), 'L': Decimal('1')}
```

#### `convert_weight(value_g)`
그램을 모든 무게 단위로 변환합니다 (**Decimal 기반**).
```python
result = convert_weight(Decimal('1000'))
# {'g': Decimal('1000'), 'kg': Decimal('1'), 't': Decimal('0.001')}
```

#### `check_answer(user_answers, correct_answers)`
사용자 입력이 정답과 일치하는지 확인합니다 (소수점 오차 허용).
**Decimal 기반 정확한 계산으로 반올림 오류를 방지합니다.**

#### `get_length_hint(user_answers, correct_answers)` (v3.0 신규)
길이 문제에서 틀린 단위만 분석하여 맞춤형 힌트 생성합니다.
```python
# 예시: cm이 틀린 경우
hints = get_length_hint(user_answers, correct_answers)
# ['❌ cm 단위 변환이 틀렸습니다.\n💡 1m = 100cm 관계를 다시 확인해보세요.']
```

#### `get_capacity_hint(user_answers, correct_answers)` (v3.0 신규)
들이 문제에서 틀린 단위에 대한 맞춤형 힌트를 생성합니다.

#### `get_weight_hint(user_answers, correct_answers)` (v3.0 신규)
무게 문제에서 틀린 단위에 대한 맞춤형 힌트를 생성합니다.

---

### `generator.py` - 문제 생성 함수

각 영역별 난수를 생성하고 임의의 단위로 문제를 제시합니다.

#### `generate_length_problem()`
- 100~100,000mm 범위의 난수 생성
- mm, cm, m, km 중 랜덤하게 선택된 단위로 제시

#### `generate_capacity_problem()`
- 10~100,000mL 범위의 난수 생성
- mL 또는 L 중 랜덤하게 선택된 단위로 제시

#### `generate_weight_problem()`
- 10,000~1,000,000g 범위의 난수 생성
- g, kg, t 중 랜덤하게 선택된 단위로 제시

---

### `streamlit_app.py` - 메인 애플리케이션

#### 주요 기능
1. **세션 상태 관리** (`st.session_state`)
   - 현재 페이지 추적
   - 문제 데이터 저장
   - 피드백 메시지 관리
   - 문제 풀이 횟수 기록

2. **페이지 구성**
   - `show_home_page()`: 초기 화면 (3가지 선택)
   - `show_length_problem()`: 길이 변환 문제 + 개념 설명
   - `show_capacity_problem()`: 들이 변환 문제 + 개념 설명
   - `show_weight_problem()`: 무게 변환 문제 + 개념 설명

3. **UI 디자인**
   - 큰 폰트로 문제 표시
   - 단위별 별도 입력 필드
   - 정답/오답 피드백 메시지
   - 성공 시 풍선 애니메이션
   - 각 영역별 개념 설명 expander

#### 입력 처리 개선 (v2.0)
- **text_input() 기반**: number_input 대신 text_input() 사용으로 반올림 제거
- **Decimal 처리**: 모든 입력값을 Decimal로 변환하여 정확한 계산
- **오류 처리**: InvalidOperation 예외 처리로 사용자 오입력 방지

---

## 🎓 학습 효과

✅ **개념 이해**: 단위 간 관계를 반복 학습  
✅ **계산 능력**: 실시간 계산 연습  
✅ **즉시 피드백**: 정답 여부를 바로 확인  
✅ **자기주도 학습**: 자유로운 속도로 진행  
✅ **재미있는 학습**: 게임 형식의 인터페이스  

---

## 🔄 향후 개선 방향

- [x] 개념 설명 기능 추가 (v2.0)
- [x] 반올림 오류 수정 (Decimal 기반 처리)
- [x] text_input 기반 입력 방식으로 변경
- [x] 오답 시 단위별 힌트 기능 추가 (v3.0)
- [ ] 점수 및 통계 기록 기능
- [ ] 난이도 선택 옵션 (쉬움/보통/어려움)
- [ ] 시간 제한 모드
- [ ] 다양한 테마 색상 지원
- [ ] 모바일 반응형 디자인 개선
- [ ] 학부모 대시보드 추가
- [ ] 학생 진도 저장 기능

---

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 공개됩니다.

---

## 👨‍💻 개발자

**GitHub Copilot**  
2025년 12월

---

## 🤝 기여하기

버그 보고나 기능 제안은 이슈를 통해 해주세요!

---

## 📧 문의사항

이 프로젝트에 대한 질문이나 피드백은 GitHub 이슈를 통해 주세요.
