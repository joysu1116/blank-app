"""
단위 변환 유틸리티 모듈
길이, 들이, 무게 단위 변환 함수 제공
Decimal을 사용하여 정확한 계산 수행
"""

from decimal import Decimal, ROUND_HALF_UP


def convert_length(value_mm):
    """
    밀리미터 기준 길이를 모든 단위로 변환 (Decimal 기반)
    Args:
        value_mm (Decimal 또는 float): 밀리미터 단위 값
    Returns:
        dict: {'mm': Decimal, 'cm': Decimal, 'm': Decimal, 'km': Decimal}
    """
    value = Decimal(str(value_mm))
    return {
        'mm': value,
        'cm': value / Decimal('10'),
        'm': value / Decimal('1000'),
        'km': value / Decimal('1000000')
    }


def convert_capacity(value_ml):
    """
    밀리리터 기준 들이를 모든 단위로 변환 (Decimal 기반)
    Args:
        value_ml (Decimal 또는 float): 밀리리터 단위 값
    Returns:
        dict: {'mL': Decimal, 'L': Decimal}
    """
    value = Decimal(str(value_ml))
    return {
        'mL': value,
        'L': value / Decimal('1000')
    }


def convert_weight(value_g):
    """
    그램 기준 무게를 모든 단위로 변환 (Decimal 기반)
    Args:
        value_g (Decimal 또는 float): 그램 단위 값
    Returns:
        dict: {'g': Decimal, 'kg': Decimal, 't': Decimal}
    """
    value = Decimal(str(value_g))
    return {
        'g': value,
        'kg': value / Decimal('1000'),
        't': value / Decimal('1000000')
    }


def check_answer(user_answers, correct_answers, tolerance='0.0001'):
    """
    사용자 입력값이 정답과 일치하는지 확인 (Decimal 기반)
    Args:
        user_answers (list): 사용자 입력 값 리스트 (문자열 또는 Decimal)
        correct_answers (list): 정답 값 리스트 (Decimal)
        tolerance (str): 소수점 오차 허용범위
    Returns:
        bool: 모든 답이 맞으면 True, 하나라도 틀리면 False
    """
    if len(user_answers) != len(correct_answers):
        return False
    
    tolerance_decimal = Decimal(tolerance)
    
    for user, correct in zip(user_answers, correct_answers):
        try:
            # 사용자 입력을 Decimal로 변환
            user_value = Decimal(str(user)) if not isinstance(user, Decimal) else user
            correct_value = Decimal(str(correct)) if not isinstance(correct, Decimal) else correct
            
            # 오차 범위 내인지 확인
            if abs(user_value - correct_value) > tolerance_decimal:
                return False
        except:
            return False
    
    return True
