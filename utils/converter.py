"""
단위 변환 유틸리티 모듈
길이, 들이, 무게 단위 변환 함수 제공
Decimal을 사용하여 정확한 계산 수행
"""

from decimal import Decimal


def convert_length(value_mm):
    """
    밀리미터 기준 길이를 모든 단위로 변환 (Decimal 기반)
    Args:
        value_mm (Decimal 또는 str): 밀리미터 단위 값
    Returns:
        dict: {'mm': Decimal, 'cm': Decimal, 'm': Decimal, 'km': Decimal}
    """
    value = Decimal(str(value_mm)) if not isinstance(value_mm, Decimal) else value_mm
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
        value_ml (Decimal 또는 str): 밀리리터 단위 값
    Returns:
        dict: {'mL': Decimal, 'L': Decimal}
    """
    value = Decimal(str(value_ml)) if not isinstance(value_ml, Decimal) else value_ml
    return {
        'mL': value,
        'L': value / Decimal('1000')
    }


def convert_weight(value_g):
    """
    그램 기준 무게를 모든 단위로 변환 (Decimal 기반)
    Args:
        value_g (Decimal 또는 str): 그램 단위 값
    Returns:
        dict: {'g': Decimal, 'kg': Decimal, 't': Decimal}
    """
    value = Decimal(str(value_g)) if not isinstance(value_g, Decimal) else value_g
    return {
        'g': value,
        'kg': value / Decimal('1000'),
        't': value / Decimal('1000000')
    }


def compare_decimal_values(user_value, correct_value, tolerance='0.0001'):
    """
    두 Decimal 값을 비교하여 일치 여부 확인
    Args:
        user_value (Decimal 또는 str): 사용자 입력값
        correct_value (Decimal): 정답값
        tolerance (str): 오차 허용범위
    Returns:
        bool: 두 값이 일치하면 True
    """
    try:
        user_dec = Decimal(str(user_value)) if not isinstance(user_value, Decimal) else user_value
        correct_dec = Decimal(str(correct_value)) if not isinstance(correct_value, Decimal) else correct_value
        tolerance_dec = Decimal(tolerance)
        
        return abs(user_dec - correct_dec) <= tolerance_dec
    except:
        return False


def get_wrong_units_and_hints(user_answers, correct_answers, units, hint_messages):
    """
    틀린 단위와 힌트 메시지를 추출
    Args:
        user_answers (list): 사용자 입력값 (Decimal 또는 str)
        correct_answers (list): 정답값 (Decimal)
        units (list): 단위 이름 리스트
        hint_messages (dict): 단위별 힌트 메시지 딕셔너리
    Returns:
        list: 틀린 단위별 힌트 메시지 리스트
    """
    hints = []
    tolerance = Decimal('0.0001')
    
    for user, correct, unit in zip(user_answers, correct_answers, units):
        try:
            user_dec = Decimal(str(user)) if not isinstance(user, Decimal) else user
            correct_dec = Decimal(str(correct)) if not isinstance(correct, Decimal) else correct
            
            if abs(user_dec - correct_dec) > tolerance:
                if unit in hint_messages:
                    hints.append(hint_messages[unit])
        except:
            pass
    
    return hints
