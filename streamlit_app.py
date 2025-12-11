"""
단위 변환 학습 Streamlit 웹앱 (v4.0)
초등학교 3~4학년 수학 '도형과 측정' 영역 학습 지원
Decimal 기반 정확한 계산 및 개별 단위 비교 로직
"""

import streamlit as st
from decimal import Decimal, InvalidOperation
import time
from utils.generator import (
    generate_length_problem,
    generate_capacity_problem,
    generate_weight_problem
)
from utils.converter import (
    compare_decimal_values,
    get_wrong_units_and_hints
)


# 페이지 설정
st.set_page_config(
    page_title="단위 변환 학습",
    page_icon="📐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS 스타일링
st.markdown("""
    <style>
    .main { padding: 2rem; }
    .title {
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 2rem;
        color: #FF6B6B;
    }
    .problem-display {
        background-color: #F0F4FF;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 1.5rem 0;
        border: 3px solid #4C6EF5;
    }
    .problem-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2C3E50;
        margin: 1rem 0;
    }
    .problem-question {
        font-size: 1.2rem;
        color: #555;
        margin: 1rem 0;
    }
    .input-section {
        background-color: #F9F9F9;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0;
    }
    .success-message {
        background-color: #D4EDDA;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 1rem 0;
        border: 2px solid #28a745;
    }
    .error-message {
        background-color: #F8D7DA;
        color: #721C24;
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 1rem 0;
        border: 2px solid #dc3545;
    }
    .hint-box {
        background-color: #E7F3FF;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)


# 개념 설명 콘텐츠
LENGTH_CONCEPT = """
### 길이의 단위
- **mm(밀리미터)**: 가장 작은 단위
- **cm(센티미터)**: 1 cm = 10 mm
- **m(미터)**: 1 m = 100 cm
- **km(킬로미터)**: 1 km = 1000 m

#### 단위 변환 관계
1 cm를 10칸으로 똑같이 나누었을 때 작은 눈금 한 칸의 길이는 **'1 mm'**라 씁니다.
- 예: 8.5 cm = 85 mm

100 cm를 **'1 m'**이라 씁니다.
- 예: 4.5 m = 450 cm

1000 m를 **'1 km'**이라 씁니다.
- 예: 1.5 km = 1500 m

#### 전체 변환 관계
**1 km = 1000 m = 100,000 cm = 1,000,000 mm**

#### 실생활 예시
- 손가락 한 마디 길이: 약 2 cm
- 교과서 가로 길이: 약 20~21 cm
- 문 높이: 약 2 m
- 학교 운동장 둘레: 약 200~400 m
- 집과 학교 사이 거리: 약 1 km
"""
CAPACITY_CONCEPT = """
### 들이의 단위
- **mL(밀리리터)**: 작은 들이 단위
- **L(리터)**: 1 L = 1000 mL

#### 단위 변환 관계
1 L = 1000 mL입니다.
- 예: 1.3 L = 1300 mL

#### 실생활 예시
- 물 한 잔: 약 200 mL
- 우유 한 팩: 약 1 L
- 큰 물통: 약 10 L
"""

WEIGHT_CONCEPT = """
### 무게의 단위
- **g(그램)**: 작은 무게 단위
- **kg(킬로그램)**: 1 kg = 1000 g
- **t(톤)**: 1 t = 1000 kg

#### 단위 변환 관계
1 kg = 1000 g입니다.
- 예: 1 kg 500 g = 1500 g

1 t = 1000 kg입니다.
- 예: 1.5 t = 1500 kg

#### 전체 변환 관계
**1 t = 1000 kg = 1,000,000 g**
 
#### 실생활 예시
- 연필 한 자루: 약 5~10 g
- 우유 한 팩(1 L): 약 1 kg
- 작은 수박 한 개: 약 5~7 kg
- 성인 몸무게: 약 50~80 kg
- 작은 차 한 대: 약 1 t
"""

# 길이 힌트 메시지
LENGTH_HINT_MESSAGES = {
    'mm': "❌ mm 단위가 틀렸습니다.\n💡 1cm = 10mm 관계를 다시 확인해보세요.",
    'cm': "❌ cm 단위가 틀렸습니다.\n💡 1m = 100cm 관계를 다시 확인해보세요.",
    'm': "❌ m 단위가 틀렸습니다.\n💡 1km = 1000m 관계를 다시 확인해보세요.",
    'km': "❌ km 단위가 틀렸습니다.\n💡 1km = 1,000,000mm 관계를 다시 확인해보세요."
}

# 들이 힌트 메시지
CAPACITY_HINT_MESSAGES = {
    'mL': "❌ mL 단위가 틀렸습니다.\n💡 1L = 1,000mL 관계를 다시 확인해보세요.",
    'L': "❌ L 단위가 틀렸습니다.\n💡 1L = 1,000mL 관계를 다시 확인해보세요."
}

# 무게 힌트 메시지
WEIGHT_HINT_MESSAGES = {
    'g': "❌ g 단위가 틀렸습니다.\n💡 1kg = 1,000g 관계를 다시 확인해보세요.",
    'kg': "❌ kg 단위가 틀렸습니다.\n💡 1kg = 1,000g, 1t = 1,000kg 관계를 다시 확인해보세요.",
    't': "❌ t 단위가 틀렸습니다.\n💡 1t = 1,000kg = 1,000,000g 관계를 다시 확인해보세요."
}


def initialize_session_state():
    """세션 상태 초기화"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'current_problem' not in st.session_state:
        st.session_state.current_problem = None
    if 'problem_count' not in st.session_state:
        st.session_state.problem_count = 0
    if 'is_correct' not in st.session_state:
        st.session_state.is_correct = None
    if 'current_hints' not in st.session_state:
        st.session_state.current_hints = []
    if 'user_last_answers' not in st.session_state:
        st.session_state.user_last_answers = []


initialize_session_state()


def show_home_page():
    """초기 화면 표시"""
    st.markdown("<div class='title'>📐 단위 변환 학습</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; font-size: 1.1rem; color: #555; margin: 2rem 0;'>
    <p><strong>다음 중 학습하고 싶은 단위를 선택하세요!</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📏 길이", key="btn_length", use_container_width=True):
            st.session_state.current_page = 'length'
            st.session_state.current_problem = generate_length_problem()
            st.session_state.problem_count = 1
            st.session_state.is_correct = None
            st.session_state.current_hints = []
            st.rerun()
    
    with col2:
        if st.button("🥤 들이", key="btn_capacity", use_container_width=True):
            st.session_state.current_page = 'capacity'
            st.session_state.current_problem = generate_capacity_problem()
            st.session_state.problem_count = 1
            st.session_state.is_correct = None
            st.session_state.current_hints = []
            st.rerun()
    
    with col3:
        if st.button("⚖️ 무게", key="btn_weight", use_container_width=True):
            st.session_state.current_page = 'weight'
            st.session_state.current_problem = generate_weight_problem()
            st.session_state.problem_count = 1
            st.session_state.is_correct = None
            st.session_state.current_hints = []
            st.rerun()


def show_length_problem():
    """길이 변환 문제 화면"""
    st.markdown("<div class='title'>📏 길이 변환</div>", unsafe_allow_html=True)
    
    with st.expander("📘 개념 설명 보기"):
        st.markdown(LENGTH_CONCEPT)
    
    problem = st.session_state.current_problem
    
    st.markdown(f"""
    <div class='problem-display'>
        <div class='problem-value'>{problem['display_value']} {problem['unit']}</div>
        <div class='problem-question'>
        다음 값을 mm, cm, m, km 단위로 변환하여<br/>
        순서대로 정답을 입력하시오.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 정답/오답 상태 표시
    if st.session_state.is_correct is not None:
        if st.session_state.is_correct:
            st.markdown(
                "<div class='success-message'>🎉 정답입니다!</div>",
                unsafe_allow_html=True
            )
            time.sleep(1)
            st.session_state.current_problem = generate_length_problem()
            st.session_state.is_correct = None
            st.session_state.current_hints = []
            st.rerun()
        else:
            st.markdown(
                "<div class='error-message'>❌ 정답이 옳지 않습니다. 다시 풀어보세요.</div>",
                unsafe_allow_html=True
            )
            if st.session_state.current_hints:
                with st.expander("🔍 힌트 보기"):
                    for hint in st.session_state.current_hints:
                        st.markdown(f"<div class='hint-box'>{hint}</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='input-section'><p><strong>정답을 입력하세요:</strong></p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        mm_input = st.text_input("mm", placeholder="예: 1000", key="length_mm")
        cm_input = st.text_input("cm", placeholder="예: 100", key="length_cm")
    with col2:
        m_input = st.text_input("m", placeholder="예: 1", key="length_m")
        km_input = st.text_input("km", placeholder="예: 0.001", key="length_km")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("정답 제출", key="submit_length", use_container_width=True):
        # 입력값 검증
        inputs = [mm_input, cm_input, m_input, km_input]
        units = ['mm', 'cm', 'm', 'km']
        user_answers = []
        valid = True
        
        for inp, unit in zip(inputs, units):
            if not inp.strip():
                st.error(f"{unit}: 값을 입력해주세요.")
                valid = False
                break
            try:
                user_answers.append(Decimal(inp))
            except InvalidOperation:
                st.error(f"{unit}: 숫자를 정확히 입력해주세요.")
                valid = False
                break
        
        if valid:
            correct_answers = problem['correct_answers']
            # 각 단위별 개별 비교
            all_correct = all(
                compare_decimal_values(user, correct)
                for user, correct in zip(user_answers, correct_answers)
            )
            
            if all_correct:
                st.session_state.is_correct = True
                st.session_state.problem_count += 1
            else:
                st.session_state.is_correct = False
                st.session_state.current_hints = get_wrong_units_and_hints(
                    user_answers, correct_answers, units, LENGTH_HINT_MESSAGES
                )
            st.rerun()
    
    st.markdown(f"<p style='text-align: center; color: #666; margin-top: 2rem;'>"
                f"<strong>풀이한 문제: {st.session_state.problem_count - 1}개</strong></p>",
                unsafe_allow_html=True)
    
    if st.button("🔄 재시작", key="restart_length", use_container_width=True):
        st.session_state.current_page = 'home'
        st.rerun()


def show_capacity_problem():
    """들이 변환 문제 화면"""
    st.markdown("<div class='title'>🥤 들이 변환</div>", unsafe_allow_html=True)
    
    with st.expander("📘 개념 설명 보기"):
        st.markdown(CAPACITY_CONCEPT)
    
    problem = st.session_state.current_problem
    
    st.markdown(f"""
    <div class='problem-display'>
        <div class='problem-value'>{problem['display_value']} {problem['unit']}</div>
        <div class='problem-question'>
        다음 값을 mL, L 단위로 변환하여<br/>
        순서대로 정답을 입력하시오.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 정답/오답 상태 표시
    if st.session_state.is_correct is not None:
        if st.session_state.is_correct:
            st.markdown(
                "<div class='success-message'>🎉 정답입니다!</div>",
                unsafe_allow_html=True
            )
            time.sleep(1)
            st.session_state.current_problem = generate_capacity_problem()
            st.session_state.is_correct = None
            st.session_state.current_hints = []
            st.rerun()
        else:
            st.markdown(
                "<div class='error-message'>❌ 정답이 옳지 않습니다. 다시 풀어보세요.</div>",
                unsafe_allow_html=True
            )
            if st.session_state.current_hints:
                with st.expander("🔍 힌트 보기"):
                    for hint in st.session_state.current_hints:
                        st.markdown(f"<div class='hint-box'>{hint}</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='input-section'><p><strong>정답을 입력하세요:</strong></p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        ml_input = st.text_input("mL", placeholder="예: 1300", key="capacity_ml")
    with col2:
        l_input = st.text_input("L", placeholder="예: 1.3", key="capacity_l")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("정답 제출", key="submit_capacity", use_container_width=True):
        inputs = [ml_input, l_input]
        units = ['mL', 'L']
        user_answers = []
        valid = True
        
        for inp, unit in zip(inputs, units):
            if not inp.strip():
                st.error(f"{unit}: 값을 입력해주세요.")
                valid = False
                break
            try:
                user_answers.append(Decimal(inp))
            except InvalidOperation:
                st.error(f"{unit}: 숫자를 정확히 입력해주세요.")
                valid = False
                break
        
        if valid:
            correct_answers = problem['correct_answers']
            all_correct = all(
                compare_decimal_values(user, correct)
                for user, correct in zip(user_answers, correct_answers)
            )
            
            if all_correct:
                st.session_state.is_correct = True
                st.session_state.problem_count += 1
            else:
                st.session_state.is_correct = False
                st.session_state.current_hints = get_wrong_units_and_hints(
                    user_answers, correct_answers, units, CAPACITY_HINT_MESSAGES
                )
            st.rerun()
    
    st.markdown(f"<p style='text-align: center; color: #666; margin-top: 2rem;'>"
                f"<strong>풀이한 문제: {st.session_state.problem_count - 1}개</strong></p>",
                unsafe_allow_html=True)
    
    if st.button("🔄 재시작", key="restart_capacity", use_container_width=True):
        st.session_state.current_page = 'home'
        st.rerun()


def show_weight_problem():
    """무게 변환 문제 화면"""
    st.markdown("<div class='title'>⚖️ 무게 변환</div>", unsafe_allow_html=True)
    
    with st.expander("📘 개념 설명 보기"):
        st.markdown(WEIGHT_CONCEPT)
    
    problem = st.session_state.current_problem
    
    st.markdown(f"""
    <div class='problem-display'>
        <div class='problem-value'>{problem['display_value']} {problem['unit']}</div>
        <div class='problem-question'>
        다음 값을 g, kg, t 단위로 변환하여<br/>
        순서대로 정답을 입력하시오.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 정답/오답 상태 표시
    if st.session_state.is_correct is not None:
        if st.session_state.is_correct:
            st.markdown(
                "<div class='success-message'>🎉 정답입니다!</div>",
                unsafe_allow_html=True
            )
            time.sleep(1)
            st.session_state.current_problem = generate_weight_problem()
            st.session_state.is_correct = None
            st.session_state.current_hints = []
            st.rerun()
        else:
            st.markdown(
                "<div class='error-message'>❌ 정답이 옳지 않습니다. 다시 풀어보세요.</div>",
                unsafe_allow_html=True
            )
            if st.session_state.current_hints:
                with st.expander("🔍 힌트 보기"):
                    for hint in st.session_state.current_hints:
                        st.markdown(f"<div class='hint-box'>{hint}</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='input-section'><p><strong>정답을 입력하세요:</strong></p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        g_input = st.text_input("g", placeholder="예: 1500", key="weight_g")
        kg_input = st.text_input("kg", placeholder="예: 1.5", key="weight_kg")
    with col2:
        t_input = st.text_input("t", placeholder="예: 0.0015", key="weight_t")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("정답 제출", key="submit_weight", use_container_width=True):
        inputs = [g_input, kg_input, t_input]
        units = ['g', 'kg', 't']
        user_answers = []
        valid = True
        
        for inp, unit in zip(inputs, units):
            if not inp.strip():
                st.error(f"{unit}: 값을 입력해주세요.")
                valid = False
                break
            try:
                user_answers.append(Decimal(inp))
            except InvalidOperation:
                st.error(f"{unit}: 숫자를 정확히 입력해주세요.")
                valid = False
                break
        
        if valid:
            correct_answers = problem['correct_answers']
            all_correct = all(
                compare_decimal_values(user, correct)
                for user, correct in zip(user_answers, correct_answers)
            )
            
            if all_correct:
                st.session_state.is_correct = True
                st.session_state.problem_count += 1
            else:
                st.session_state.is_correct = False
                st.session_state.current_hints = get_wrong_units_and_hints(
                    user_answers, correct_answers, units, WEIGHT_HINT_MESSAGES
                )
            st.rerun()
    
    st.markdown(f"<p style='text-align: center; color: #666; margin-top: 2rem;'>"
                f"<strong>풀이한 문제: {st.session_state.problem_count - 1}개</strong></p>",
                unsafe_allow_html=True)
    
    if st.button("🔄 재시작", key="restart_weight", use_container_width=True):
        st.session_state.current_page = 'home'
        st.rerun()


# 메인 앱 로직
if st.session_state.current_page == 'home':
    show_home_page()
elif st.session_state.current_page == 'length':
    show_length_problem()
elif st.session_state.current_page == 'capacity':
    show_capacity_problem()
elif st.session_state.current_page == 'weight':
    show_weight_problem()
