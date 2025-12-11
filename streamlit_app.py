"""
단위 변환 학습 Streamlit 웹앱
초등학교 3~4학년 수학 '도형과 측정' 영역 학습 지원
Decimal을 사용한 정확한 계산 처리
"""

import streamlit as st
from decimal import Decimal, InvalidOperation
from utils.generator import (
    generate_length_problem,
    generate_capacity_problem,
    generate_weight_problem
)
from utils.converter import (
    check_answer,
    get_length_hint,
    get_capacity_hint,
    get_weight_hint
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
    .main {
        padding: 2rem;
    }
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
    .unit-input {
        display: flex;
        align-items: center;
        margin: 0.8rem 0;
        gap: 1rem;
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
    }
    .button-group {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)


# 세션 상태 초기화
def initialize_session_state():
    """세션 상태 초기화 함수"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'current_problem' not in st.session_state:
        st.session_state.current_problem = None
    if 'feedback_message' not in st.session_state:
        st.session_state.feedback_message = ''
    if 'problem_count' not in st.session_state:
        st.session_state.problem_count = 0
    if 'current_hints' not in st.session_state:
        st.session_state.current_hints = []


initialize_session_state()


# 개념 설명 콘텐츠
LENGTH_CONCEPT = """
### 길이의 단위
- **mm(밀리미터)**: 가장 작은 단위
- **cm(센티미터)**: 1 cm = 10 mm
- **m(미터)**: 1 m = 100 cm
- **km(킬로미터)**: 1 km = 1000 m

#### 단위 변환 관계
1 cm를 10칸으로 똑같이 나누었을 때 작은 눈금 한 칸의 길이는 **'1 mm'**라 씁니다.
- 예: 8.5 cm = 8.5 센티미터 = 8cm 5mm = 85 mm

100 cm를 **'1 m'**이라 씁니다.
- 예: 4.5 m = 4.5 미터 = 4 m 50 cm = 450 cm

1000 m를 **'1 km'**이라 씁니다.
- 예: 1.5 km = 1.5 킬로미터 = 1 km 500 m = 1500 m

#### 전체 변환 관계
**1 km = 1000 m = 100,000 cm = 1,000,000 mm**
"""

CAPACITY_CONCEPT = """
### 들이의 단위
- **mL(밀리리터)**: 작은 들이 단위
- **L(리터)**: 1 L = 1000 mL

#### 단위 변환 관계
1 L = 1000 mL입니다.
- 예: 1.3 L = 1.3 리터 = 1 L 300 mL = 1300 mL

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
- 예: 1 kg 500 g = 1 킬로그램 500 그램 = 1500 g

1 t = 1000 kg입니다.
- 예: 1.5 t = 1.5톤 = 1 t 500 kg = 1500 kg

#### 전체 변환 관계
**1 t = 1000 kg = 1,000,000 g**

#### 실생활 예시
- 달걀 한 개: 약 60 g
- 사과 한 개: 약 200 g
- 어린이 체중: 약 30 kg
- 자동차: 약 1 t
"""


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
        if st.button("📏 길이", key="btn_length", use_container_width=True, 
                     help="mm, cm, m, km 단위 변환 학습"):
            st.session_state.current_page = 'length'
            st.session_state.current_problem = generate_length_problem()
            st.session_state.problem_count = 1
            st.rerun()
    
    with col2:
        if st.button("🥤 들이", key="btn_capacity", use_container_width=True,
                     help="mL, L 단위 변환 학습"):
            st.session_state.current_page = 'capacity'
            st.session_state.current_problem = generate_capacity_problem()
            st.session_state.problem_count = 1
            st.rerun()
    
    with col3:
        if st.button("⚖️ 무게", key="btn_weight", use_container_width=True,
                     help="g, kg, t 단위 변환 학습"):
            st.session_state.current_page = 'weight'
            st.session_state.current_problem = generate_weight_problem()
            st.session_state.problem_count = 1
            st.rerun()


def show_length_problem():
    """길이 변환 문제 화면"""
    st.markdown("<div class='title'>📏 길이 변환</div>", unsafe_allow_html=True)
    
    # 개념 설명 expander
    with st.expander("📘 개념 설명 보기"):
        st.markdown(LENGTH_CONCEPT)
    
    problem = st.session_state.current_problem
    
    # 문제 표시
    st.markdown(f"""
    <div class='problem-display'>
        <div class='problem-value'>{problem['display_value']:.1f} {problem['unit']}</div>
        <div class='problem-question'>
        다음 값을 mm, cm, m, km 단위로 변환하여<br/>
        순서대로 정답을 입력하시오.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 피드백 메시지 표시
    if st.session_state.feedback_message:
        if "정답" in st.session_state.feedback_message:
            st.markdown(
                f"<div class='success-message'>{st.session_state.feedback_message}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='error-message'>{st.session_state.feedback_message}</div>",
                unsafe_allow_html=True
            )
            
            # 오답 시 힌트 표시
            if 'current_hints' in st.session_state and st.session_state.current_hints:
                with st.expander("🔍 힌트 보기"):
                    for hint in st.session_state.current_hints:
                        st.info(hint)
    
    # 입력 필드 - text_input으로 변경
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    st.markdown("**정답을 입력하세요:**")
    
    col1, col2 = st.columns(2)
    with col1:
        mm_input = st.text_input("mm", placeholder="예: 1000", key="length_mm")
        cm_input = st.text_input("cm", placeholder="예: 100", key="length_cm")
    
    with col2:
        m_input = st.text_input("m", placeholder="예: 1", key="length_m")
        km_input = st.text_input("km", placeholder="예: 0.001", key="length_km")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 제출 버튼
    if st.button("정답 제출", key="submit_length", use_container_width=True):
        # 입력값 검증 및 Decimal 변환
        user_answers = []
        valid_input = True
        
        for input_val, unit_name in [(mm_input, 'mm'), (cm_input, 'cm'), 
                                      (m_input, 'm'), (km_input, 'km')]:
            if not input_val.strip():
                st.error(f"{unit_name}: 값을 입력해주세요.")
                valid_input = False
                break
            try:
                user_answers.append(Decimal(input_val))
            except InvalidOperation:
                st.error(f"{unit_name}: 숫자를 정확히 입력해주세요.")
                valid_input = False
                break
        
        if valid_input:
            correct_answers = problem['correct_answers']
            
            if check_answer(user_answers, correct_answers):
                st.session_state.feedback_message = "🎉 정답입니다!"
                st.session_state.problem_count += 1
                st.balloons()
                
                # 2초 후 새 문제 생성
                import time
                time.sleep(1)
                st.session_state.current_problem = generate_length_problem()
                st.session_state.feedback_message = ''
                st.rerun()
            else:
                st.session_state.feedback_message = "❌ 정답이 옳지 않습니다. 다시 풀어보세요."
                st.session_state.current_hints = get_length_hint(user_answers, correct_answers)
                st.rerun()
    
    # 통계
    st.markdown(f"<p style='text-align: center; color: #666; margin-top: 2rem;'>"
                f"<strong>풀이한 문제: {st.session_state.problem_count - 1}개</strong></p>",
                unsafe_allow_html=True)
    
    # 재시작 버튼
    if st.button("🔄 재시작", key="restart_length", use_container_width=True):
        st.session_state.current_page = 'home'
        st.session_state.current_problem = None
        st.session_state.feedback_message = ''
        st.session_state.problem_count = 0
        st.rerun()


def show_capacity_problem():
    """들이 변환 문제 화면"""
    st.markdown("<div class='title'>🥤 들이 변환</div>", unsafe_allow_html=True)
    
    # 개념 설명 expander
    with st.expander("📘 개념 설명 보기"):
        st.markdown(CAPACITY_CONCEPT)
    
    problem = st.session_state.current_problem
    
    # 문제 표시
    st.markdown(f"""
    <div class='problem-display'>
        <div class='problem-value'>{problem['display_value']:.1f} {problem['unit']}</div>
        <div class='problem-question'>
        다음 값을 mL, L 단위로 변환하여<br/>
        순서대로 정답을 입력하시오.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 피드백 메시지 표시
    if st.session_state.feedback_message:
        if "정답" in st.session_state.feedback_message:
            st.markdown(
                f"<div class='success-message'>{st.session_state.feedback_message}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='error-message'>{st.session_state.feedback_message}</div>",
                unsafe_allow_html=True
            )
            
            # 오답 시 힌트 표시
            if 'current_hints' in st.session_state and st.session_state.current_hints:
                with st.expander("🔍 힌트 보기"):
                    for hint in st.session_state.current_hints:
                        st.info(hint)
    
    # 입력 필드 - text_input으로 변경
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    st.markdown("**정답을 입력하세요:**")
    
    col1, col2 = st.columns(2)
    with col1:
        ml_input = st.text_input("mL", placeholder="예: 1300", key="capacity_ml")
    with col2:
        l_input = st.text_input("L", placeholder="예: 1.3", key="capacity_l")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 제출 버튼
    if st.button("정답 제출", key="submit_capacity", use_container_width=True):
        # 입력값 검증 및 Decimal 변환
        user_answers = []
        valid_input = True
        
        for input_val, unit_name in [(ml_input, 'mL'), (l_input, 'L')]:
            if not input_val.strip():
                st.error(f"{unit_name}: 값을 입력해주세요.")
                valid_input = False
                break
            try:
                user_answers.append(Decimal(input_val))
            except InvalidOperation:
                st.error(f"{unit_name}: 숫자를 정확히 입력해주세요.")
                valid_input = False
                break
        
        if valid_input:
            correct_answers = problem['correct_answers']
            
            if check_answer(user_answers, correct_answers):
                st.session_state.feedback_message = "🎉 정답입니다!"
                st.session_state.problem_count += 1
                st.balloons()
                
                # 2초 후 새 문제 생성
                import time
                time.sleep(1)
                st.session_state.current_problem = generate_capacity_problem()
                st.session_state.feedback_message = ''
                st.rerun()
            else:
                st.session_state.feedback_message = "❌ 정답이 옳지 않습니다. 다시 풀어보세요."
                st.session_state.current_hints = get_capacity_hint(user_answers, correct_answers)
                st.rerun()
    
    # 통계
    st.markdown(f"<p style='text-align: center; color: #666; margin-top: 2rem;'>"
                f"<strong>풀이한 문제: {st.session_state.problem_count - 1}개</strong></p>",
                unsafe_allow_html=True)
    
    # 재시작 버튼
    if st.button("🔄 재시작", key="restart_capacity", use_container_width=True):
        st.session_state.current_page = 'home'
        st.session_state.current_problem = None
        st.session_state.feedback_message = ''
        st.session_state.problem_count = 0
        st.rerun()


def show_weight_problem():
    """무게 변환 문제 화면"""
    st.markdown("<div class='title'>⚖️ 무게 변환</div>", unsafe_allow_html=True)
    
    # 개념 설명 expander
    with st.expander("📘 개념 설명 보기"):
        st.markdown(WEIGHT_CONCEPT)
    
    problem = st.session_state.current_problem
    
    # 문제 표시
    st.markdown(f"""
    <div class='problem-display'>
        <div class='problem-value'>{problem['display_value']:.1f} {problem['unit']}</div>
        <div class='problem-question'>
        다음 값을 g, kg, t 단위로 변환하여<br/>
        순서대로 정답을 입력하시오.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 피드백 메시지 표시
    if st.session_state.feedback_message:
        if "정답" in st.session_state.feedback_message:
            st.markdown(
                f"<div class='success-message'>{st.session_state.feedback_message}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='error-message'>{st.session_state.feedback_message}</div>",
                unsafe_allow_html=True
            )
            
            # 오답 시 힌트 표시
            if 'current_hints' in st.session_state and st.session_state.current_hints:
                with st.expander("🔍 힌트 보기"):
                    for hint in st.session_state.current_hints:
                        st.info(hint)
    
    # 입력 필드 - text_input으로 변경
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    st.markdown("**정답을 입력하세요:**")
    
    col1, col2 = st.columns(2)
    with col1:
        g_input = st.text_input("g", placeholder="예: 1500", key="weight_g")
        kg_input = st.text_input("kg", placeholder="예: 1.5", key="weight_kg")
    
    with col2:
        t_input = st.text_input("t", placeholder="예: 0.0015", key="weight_t")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 제출 버튼
    if st.button("정답 제출", key="submit_weight", use_container_width=True):
        # 입력값 검증 및 Decimal 변환
        user_answers = []
        valid_input = True
        
        for input_val, unit_name in [(g_input, 'g'), (kg_input, 'kg'), (t_input, 't')]:
            if not input_val.strip():
                st.error(f"{unit_name}: 값을 입력해주세요.")
                valid_input = False
                break
            try:
                user_answers.append(Decimal(input_val))
            except InvalidOperation:
                st.error(f"{unit_name}: 숫자를 정확히 입력해주세요.")
                valid_input = False
                break
        
        if valid_input:
            correct_answers = problem['correct_answers']
            
            if check_answer(user_answers, correct_answers):
                st.session_state.feedback_message = "🎉 정답입니다!"
                st.session_state.problem_count += 1
                st.balloons()
                
                # 2초 후 새 문제 생성
                import time
                time.sleep(1)
                st.session_state.current_problem = generate_weight_problem()
                st.session_state.feedback_message = ''
                st.rerun()
            else:
                st.session_state.feedback_message = "❌ 정답이 옳지 않습니다. 다시 풀어보세요."
                st.session_state.current_hints = get_weight_hint(user_answers, correct_answers)
                st.rerun()
    
    # 통계
    st.markdown(f"<p style='text-align: center; color: #666; margin-top: 2rem;'>"
                f"<strong>풀이한 문제: {st.session_state.problem_count - 1}개</strong></p>",
                unsafe_allow_html=True)
    
    # 재시작 버튼
    if st.button("🔄 재시작", key="restart_weight", use_container_width=True):
        st.session_state.current_page = 'home'
        st.session_state.current_problem = None
        st.session_state.feedback_message = ''
        st.session_state.problem_count = 0
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
