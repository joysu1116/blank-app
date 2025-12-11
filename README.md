# 📐 단위 변환 학습 웹앱 (v4.0)

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

## ✨ v4.0 주요 개선사항

### 🔧 핵심 버그 수정
- ✅ **Decimal 기반 전면 재구성**: 부동소수점 오차 완전 제거
  - 문제 생성: 정수 기반으로 변경 → float 오차 제거
  - 정답 저장: 모두 Decimal로 통일
  - 입력 처리: text_input → Decimal 변환
  - 비교 로직: 개별 단위별 Decimal 비교

- ✅ **정답 판정 로직 재설계**
  - 이전: 리스트 전체 비교 (불안정)
  - 현재: 개별 단위별 비교 (정확)
  - 0.0001 오차 허용범위

- ✅ **오답 시 힌트 기능 안정화**
  - 틀린 단위만 자동으로 정확히 감지
  - expander로 힌트 표시 (항상 작동)
  - 단위별 맞춤형 학습 가이드

### 💡 사용자 경험 개선
- 정답/오답 UI 명확하게 분리
- is_correct 상태 저장으로 예측 가능한 흐름
- 힌트는 오답일 때만 표시

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
 
**실생활 예시 (길이):**
- 손가락 한 마디 길이: 약 2 cm
- 교과서 가로 길이: 약 20~21 cm
- 문 높이: 약 2 m
- 학교 운동장 둘레: 약 200~400 m
- 집과 학교 사이 거리: 약 1 km

**들이 영역:**
- mL, L의 단위 관계  
- 1 L = 1000 mL
- 실생활 예시

**무게 영역:**
- g, kg, t의 단위 관계
- 1 kg = 1000 g, 1 t = 1000 kg
- 실생활 예시
 
**실생활 예시 (무게):**
- 연필 한 자루: 약 5~10 g
- 우유 한 팩(1 L): 약 1 kg
- 작은 수박 한 개: 약 5~7 kg
- 성인 몸무게: 약 50~80 kg
- 작은 차 한 대: 약 1 t

### 3️⃣ **오답 시 맞춤형 힌트 기능**
오답일 경우 "🔍 힌트 보기" expander가 나타납니다:
- **정확한 단위 분석**: Decimal 비교로 틀린 단위만 판별
- **맞춤형 가이드**: 해당 단위에 대한 구체적인 학습 팁
- **예시**:
  - mm이 틀렸다면: "1cm = 10mm 관계를 다시 확인해보세요."
  - t가 틀렸다면: "1t = 1,000kg = 1,000,000g 관계를 다시 확인해보세요."

### 4️⃣ **길이 변환 문제**
```
문제 예: 83421mm를 mm, cm, m, km으로 변환하세요
- 범위: 100mm ~ 100,000mm
- 정답이면: 새로운 난수 문제 자동 생성
- 오답이면: 메시지 + 힌트 표시
```

### 5️⃣ **들이 변환 문제**
```
문제 예: 50000mL을 mL, L로 변환하세요
- 범위: 10mL ~ 100,000mL
- 정답이면: 새로운 난수 문제 자동 생성
- 오답이면: 메시지 + 힌트 표시
```

### 6️⃣ **무게 변환 문제**
```
문제 예: 500000g을 g, kg, t로 변환하세요
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
├── streamlit_app.py          # 메인 Streamlit 애플리케이션 (v4.0)
├── utils/
│   ├── __init__.py           # 패키지 초기화
│   ├── converter.py          # 단위 변환 함수 (Decimal 기반)
│   └── generator.py          # 문제 생성 함수 (Decimal 기반)
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
| Decimal | 표준라이브러리 | 정확한 수치 계산 |

---

## 📊 코드 설명

### `converter.py` - 단위 변환 함수 (v4.0)

#### `convert_length(value_mm)`
밀리미터를 모든 길이 단위로 변환합니다 (**Decimal 기반**).
```python
from decimal import Decimal
result = convert_length(Decimal('100000'))
# {'mm': Decimal('100000'), 'cm': Decimal('10000'), 'm': Decimal('100'), 'km': Decimal('0.1')}
```

#### `convert_capacity(value_ml)`
밀리리터를 모든 들이 단위로 변환합니다 (**Decimal 기반**).
```python
result = convert_capacity(Decimal('50000'))
# {'mL': Decimal('50000'), 'L': Decimal('50')}
```

#### `convert_weight(value_g)`
그램을 모든 무게 단위로 변환합니다 (**Decimal 기반**).
```python
result = convert_weight(Decimal('500000'))
# {'g': Decimal('500000'), 'kg': Decimal('500'), 't': Decimal('0.5')}
```

#### `compare_decimal_values(user_value, correct_value)` (v4.0 신규)
두 Decimal 값을 정확하게 비교합니다 (0.0001 오차 허용).
```python
# 정답 비교 (이제 정확함!)
is_correct = compare_decimal_values(Decimal('100'), Decimal('100'))  # True
```

#### `get_wrong_units_and_hints(user_answers, correct_answers, units, hint_messages)` (v4.0 신규)
틀린 단위를 감지하고 해당하는 힌트 메시지를 반환합니다.
```python
hints = get_wrong_units_and_hints(user_answers, correct_answers, units, hint_dict)
# [힌트 메시지 리스트]
```

### `generator.py` - 문제 생성 함수 (v4.0)

각 영역별 난수를 생성하고 Decimal 기반으로 정확한 문제를 생성합니다.

#### `generate_length_problem()`
- 100~100,000mm 범위의 정수 난수 생성 (float 오차 제거)
- mm, cm, m, km 중 랜덤하게 선택된 단위로 제시
- 모든 정답은 Decimal

#### `generate_capacity_problem()`
- 10~100,000mL 범위의 정수 난수 생성
- mL 또는 L 중 랜덤하게 선택된 단위로 제시
- 모든 정답은 Decimal

#### `generate_weight_problem()`
- 10,000~1,000,000g 범위의 정수 난수 생성
- g, kg, t 중 랜덤하게 선택된 단위로 제시
- 모든 정답은 Decimal

### `streamlit_app.py` - 메인 애플리케이션 (v4.0)

#### 주요 기능
1. **세션 상태 관리** (`st.session_state`)
   - `is_correct`: 정답 여부 (True/False/None)
   - `current_problem`: 현재 문제
   - `current_hints`: 틀린 단위별 힌트 리스트

2. **정답/오답 처리**
   - 각 단위별 개별 비교: `compare_decimal_values()`
   - 모든 단위가 정답이면 정답 처리
   - 하나라도 틀리면 오답 + 힌트 생성

3. **UI 분리**
   - 정답: 녹색 메시지 + 자동으로 다음 문제 생성
   - 오답: 빨간색 메시지 + expander의 힌트 표시

#### 입력 처리 (v4.0)
```python
# 사용자 입력 (text_input)
user_input = st.text_input("mm", placeholder="예: 1000")

# Decimal 변환
try:
    user_value = Decimal(user_input)
except InvalidOperation:
    st.error("숫자를 정확히 입력해주세요.")

# 비교
is_correct = compare_decimal_values(user_value, correct_value)
```

---

## 🎓 학습 효과

✅ **개념 이해**: 단위 간 관계를 반복 학습  
✅ **계산 능력**: 정확한 Decimal 기반 계산 연습  
✅ **즉시 피드백**: 정답 여부를 바로 확인  
✅ **자기주도 학습**: 자유로운 속도로 진행  
✅ **게임 형식**: 풍선 애니메이션으로 재미있는 학습  
✅ **맞춤형 가이드**: 틀린 부분만 집중 학습  

---

## 🔄 버전 히스토리

### v4.0 (2025-12-11) - 주요 버그 수정
- ✅ Decimal 기반 전면 재구성
- ✅ 정답 판정 로직 완전 재설계
- ✅ 부동소수점 오차 완전 제거
- ✅ 힌트 기능 안정화
- ✅ is_correct 상태 기반 UI 분리

### v3.0 - 힌트 기능 추가
- 오답 시 단위별 힌트 제공

### v2.0 - 개념 설명 추가
- 영역별 개념 설명 expander

### v1.0 - 초기 버전
- 기본 단위 변환 기능

---

## 📧 문제 해결 가이드

### Q: "정답을 입력했는데 틀렸다고 나온다"
**A (v4.0 해결)**: Decimal 기반 정확한 비교로 이제 해결됨

### Q: "힌트 보기가 나타나지 않는다"
**A (v4.0 해결)**: is_correct 상태 기반으로 재설계되어 이제 항상 나타남

### Q: "소수점 입력 시 값이 자동으로 반올림된다"
**A (v4.0 해결)**: text_input 기반으로 변경하여 완전히 제거됨

---

## 🔮 향후 개선 방향

- [ ] 점수 및 통계 기록 기능
- [ ] 난이도 선택 옵션 (쉬움/보통/어려움)
- [ ] 시간 제한 모드
- [ ] 다양한 테마 색상 지원
- [ ] 모바일 반응형 디자인 개선
- [ ] 학부모 대시보드 추가
- [ ] 학생 진도 저장 기능

---

## 👨‍💻 개발자

**GitHub Copilot**  
2025년 12월

---

## 🤝 기여하기

버그 보고나 기능 제안은 이슈를 통해 해주세요!

---

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 공개됩니다.
