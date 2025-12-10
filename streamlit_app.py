"""
단위 변환 학습 Streamlit 웹앱
초등학교 3~4학년 수학 '도형과 측정' 영역 학습 지원
"""

import streamlit as st
from utils.generator import (
    generate_length_problem,
    generate_capacity_problem,
    generate_weight_problem
)
from utils.converter import check_answer


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
    
    # 입력 필드
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        mm_input = st.number_input("mm", value=None, placeholder="숫자 입력", key="length_mm")
        cm_input = st.number_input("cm", value=None, placeholder="숫자 입력", key="length_cm")
    
    with col2:
        m_input = st.number_input("m", value=None, placeholder="숫자 입력", key="length_m")
        km_input = st.number_input("km", value=None, placeholder="숫자 입력", key="length_km")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 제출 버튼
    if st.button("정답 제출", key="submit_length", use_container_width=True):
        user_answers = [mm_input, cm_input, m_input, km_input]
        correct_answers = problem['correct_answers']
        
        if all(ans is not None for ans in user_answers):
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
                st.rerun()
        else:
            st.warning("모든 값을 입력해주세요.")
    
    # 통계
    st.markdown(f"<p style='text-align: center; color: #666; margin-top: 2rem;'>"
                f"<strong>풀이한 문제: {st.session_state.problem_count - 1}개</strong></p>",
                unsafe_allow_html=True)
    
    # 재시작 버튼
    if st.button("🔄 재시작", key="restart", use_container_width=True):
        st.session_state.current_page = 'home'
        st.session_state.current_problem = None
        st.session_state.feedback_message = ''
        st.session_state.problem_count = 0
        st.rerun()


def show_capacity_problem():
    """들이 변환 문제 화면"""
    st.markdown("<div class='title'>🥤 들이 변환</div>", unsafe_allow_html=True)
    
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
    
    # 입력 필드
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        ml_input = st.number_input("mL", value=None, placeholder="숫자 입력", key="capacity_ml")
    with col2:
        l_input = st.number_input("L", value=None, placeholder="숫자 입력", key="capacity_l")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 제출 버튼
    if st.button("정답 제출", key="submit_capacity", use_container_width=True):
        user_answers = [ml_input, l_input]
        correct_answers = problem['correct_answers']
        
        if all(ans is not None for ans in user_answers):
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
                st.rerun()
        else:
            st.warning("모든 값을 입력해주세요.")
    
    # 통계
    st.markdown(f"<p style='text-align: center; color: #666; margin-top: 2rem;'>"
                f"<strong>풀이한 문제: {st.session_state.problem_count - 1}개</strong></p>",
                unsafe_allow_html=True)
    
    # 재시작 버튼
    if st.button("🔄 재시작", key="restart", use_container_width=True):
        st.session_state.current_page = 'home'
        st.session_state.current_problem = None
        st.session_state.feedback_message = ''
        st.session_state.problem_count = 0
        st.rerun()


def show_weight_problem():
    """무게 변환 문제 화면"""
    st.markdown("<div class='title'>⚖️ 무게 변환</div>", unsafe_allow_html=True)
    
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
    
    # 입력 필드
    st.markdown("<div class='input-section'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        g_input = st.number_input("g", value=None, placeholder="숫자 입력", key="weight_g")
        kg_input = st.number_input("kg", value=None, placeholder="숫자 입력", key="weight_kg")
    
    with col2:
        t_input = st.number_input("t", value=None, placeholder="숫자 입력", key="weight_t")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 제출 버튼
    if st.button("정답 제출", key="submit_weight", use_container_width=True):
        user_answers = [g_input, kg_input, t_input]
        correct_answers = problem['correct_answers']
        
        if all(ans is not None for ans in user_answers):
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
                st.rerun()
        else:
            st.warning("모든 값을 입력해주세요.")
    
    # 통계
    st.markdown(f"<p style='text-align: center; color: #666; margin-top: 2rem;'>"
                f"<strong>풀이한 문제: {st.session_state.problem_count - 1}개</strong></p>",
                unsafe_allow_html=True)
    
    # 재시작 버튼
    if st.button("🔄 재시작", key="restart", use_container_width=True):
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
