"""
단위 변환 유틸리티 모듈
길이, 들이, 무게 단위 변환 함수 제공
"""

def convert_length(value_mm):
    """
    밀리미터 기준 길이를 모든 단위로 변환
    Args:
        value_mm (float): 밀리미터 단위 값
    Returns:
        dict: {'mm': float, 'cm': float, 'm': float, 'km': float}
    """
    return {
        'mm': value_mm,
        'cm': value_mm / 10,
        'm': value_mm / 1000,
        'km': value_mm / 1000000
    }


def convert_capacity(value_ml):
    """
    밀리리터 기준 들이를 모든 단위로 변환
    Args:
        value_ml (float): 밀리리터 단위 값
    Returns:
        dict: {'mL': float, 'L': float}
    """
    return {
        'mL': value_ml,
        'L': value_ml / 1000
    }


def convert_weight(value_g):
    """
    그램 기준 무게를 모든 단위로 변환
    Args:
        value_g (float): 그램 단위 값
    Returns:
        dict: {'g': float, 'kg': float, 't': float}
    """
    return {
        'g': value_g,
        'kg': value_g / 1000,
        't': value_g / 1000000
    }


def check_answer(user_answers, correct_answers, tolerance=0.0001):
    """
    사용자 입력값이 정답과 일치하는지 확인
    Args:
        user_answers (list): 사용자 입력 값 리스트
        correct_answers (list): 정답 값 리스트
        tolerance (float): 소수점 오차 허용범위
    Returns:
        bool: 모든 답이 맞으면 True, 하나라도 틀리면 False
    """
    if len(user_answers) != len(correct_answers):
        return False
    
    for user, correct in zip(user_answers, correct_answers):
        try:
            if abs(float(user) - float(correct)) > tolerance:
                return False
        except (ValueError, TypeError):
            return False
    
    return True
