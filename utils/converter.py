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


def get_length_hint(user_answers, correct_answers):
    """
    길이 문제에서 틀린 단위에 대한 힌트 생성
    Args:
        user_answers (list): [mm, cm, m, km]
        correct_answers (list): [mm, cm, m, km]
    Returns:
        list: 틀린 단위별 힌트 메시지
    """
    units = ['mm', 'cm', 'm', 'km']
    hints = []
    tolerance = Decimal('0.0001')
    
    for i, (user, correct) in enumerate(zip(user_answers, correct_answers)):
        try:
            user_value = Decimal(str(user)) if not isinstance(user, Decimal) else user
            correct_value = Decimal(str(correct)) if not isinstance(correct, Decimal) else correct
            
            if abs(user_value - correct_value) > tolerance:
                unit = units[i]
                if unit == 'mm':
                    hints.append(f"❌ {unit} 단위 변환이 틀렸습니다.\n💡 1cm = 10mm 관계를 다시 확인해보세요.")
                elif unit == 'cm':
                    hints.append(f"❌ {unit} 단위 변환이 틀렸습니다.\n💡 1m = 100cm 관계를 다시 확인해보세요.")
                elif unit == 'm':
                    hints.append(f"❌ {unit} 단위 변환이 틀렸습니다.\n💡 1km = 1000m 관계를 다시 확인해보세요.")
                elif unit == 'km':
                    hints.append(f"❌ {unit} 단위 변환이 틀렸습니다.\n💡 1km = 1,000,000mm 관계를 다시 확인해보세요.")
        except:
            pass
    
    return hints


def get_capacity_hint(user_answers, correct_answers):
    """
    들이 문제에서 틀린 단위에 대한 힌트 생성
    Args:
        user_answers (list): [mL, L]
        correct_answers (list): [mL, L]
    Returns:
        list: 틀린 단위별 힌트 메시지
    """
    units = ['mL', 'L']
    hints = []
    tolerance = Decimal('0.0001')
    
    for i, (user, correct) in enumerate(zip(user_answers, correct_answers)):
        try:
            user_value = Decimal(str(user)) if not isinstance(user, Decimal) else user
            correct_value = Decimal(str(correct)) if not isinstance(correct, Decimal) else correct
            
            if abs(user_value - correct_value) > tolerance:
                unit = units[i]
                if unit == 'mL':
                    hints.append(f"❌ {unit} 단위 변환이 틀렸습니다.\n💡 1L = 1,000mL 관계를 다시 확인해보세요.")
                elif unit == 'L':
                    hints.append(f"❌ {unit} 단위 변환이 틀렸습니다.\n💡 1L = 1,000mL 관계를 다시 확인해보세요.")
        except:
            pass
    
    return hints


def get_weight_hint(user_answers, correct_answers):
    """
    무게 문제에서 틀린 단위에 대한 힌트 생성
    Args:
        user_answers (list): [g, kg, t]
        correct_answers (list): [g, kg, t]
    Returns:
        list: 틀린 단위별 힌트 메시지
    """
    units = ['g', 'kg', 't']
    hints = []
    tolerance = Decimal('0.0001')
    
    for i, (user, correct) in enumerate(zip(user_answers, correct_answers)):
        try:
            user_value = Decimal(str(user)) if not isinstance(user, Decimal) else user
            correct_value = Decimal(str(correct)) if not isinstance(correct, Decimal) else correct
            
            if abs(user_value - correct_value) > tolerance:
                unit = units[i]
                if unit == 'g':
                    hints.append(f"❌ {unit} 단위 변환이 틀렸습니다.\n💡 1kg = 1,000g 관계를 다시 확인해보세요.")
                elif unit == 'kg':
                    hints.append(f"❌ {unit} 단위 변환이 틀렸습니다.\n💡 1kg = 1,000g, 1t = 1,000kg 관계를 다시 확인해보세요.")
                elif unit == 't':
                    hints.append(f"❌ {unit} 단위 변환이 틀렸습니다.\n💡 1t = 1,000kg = 1,000,000g 관계를 다시 확인해보세요.")
        except:
            pass
    
    return hints
