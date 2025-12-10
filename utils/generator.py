"""
문제 생성 유틸리티 모듈
각 단위 변환 영역에 대한 랜덤 문제 생성
"""

import random
from utils.converter import convert_length, convert_capacity, convert_weight


def generate_length_problem():
    """
    길이 변환 문제 생성 (100mm ~ 100000mm 범위)
    Returns:
        dict: {
            'value_mm': float,
            'unit': str (mm, cm, m, km 중 하나),
            'display_value': float,
            'correct_answers': dict
        }
    """
    # 100mm ~ 100000mm 범위의 난수 생성
    value_mm = random.uniform(100, 100000)
    
    # 문제 제시 단위 랜덤 선택 (mm, cm, m, km 중 하나)
    units = ['mm', 'cm', 'm', 'km']
    present_unit = random.choice(units)
    
    # 선택한 단위로 값 변환
    conversions = convert_length(value_mm)
    display_value = conversions[present_unit]
    
    # 정답 (mm, cm, m, km 순서)
    correct_answers = [
        conversions['mm'],
        conversions['cm'],
        conversions['m'],
        conversions['km']
    ]
    
    return {
        'value_mm': value_mm,
        'unit': present_unit,
        'display_value': display_value,
        'correct_answers': correct_answers
    }


def generate_capacity_problem():
    """
    들이 변환 문제 생성 (10mL ~ 100000mL 범위)
    Returns:
        dict: {
            'value_ml': float,
            'unit': str (mL 또는 L 중 하나),
            'display_value': float,
            'correct_answers': dict
        }
    """
    # 10mL ~ 100000mL 범위의 난수 생성
    value_ml = random.uniform(10, 100000)
    
    # 문제 제시 단위 랜덤 선택 (mL 또는 L 중 하나)
    present_unit = random.choice(['mL', 'L'])
    
    # 선택한 단위로 값 변환
    conversions = convert_capacity(value_ml)
    display_value = conversions[present_unit]
    
    # 정답 (mL, L 순서)
    correct_answers = [
        conversions['mL'],
        conversions['L']
    ]
    
    return {
        'value_ml': value_ml,
        'unit': present_unit,
        'display_value': display_value,
        'correct_answers': correct_answers
    }


def generate_weight_problem():
    """
    무게 변환 문제 생성 (10000g ~ 1000000g 범위)
    Returns:
        dict: {
            'value_g': float,
            'unit': str (g, kg, t 중 하나),
            'display_value': float,
            'correct_answers': dict
        }
    """
    # 10000g ~ 1000000g 범위의 난수 생성
    value_g = random.uniform(10000, 1000000)
    
    # 문제 제시 단위 랜덤 선택 (g, kg, t 중 하나)
    units = ['g', 'kg', 't']
    present_unit = random.choice(units)
    
    # 선택한 단위로 값 변환
    conversions = convert_weight(value_g)
    display_value = conversions[present_unit]
    
    # 정답 (g, kg, t 순서)
    correct_answers = [
        conversions['g'],
        conversions['kg'],
        conversions['t']
    ]
    
    return {
        'value_g': value_g,
        'unit': present_unit,
        'display_value': display_value,
        'correct_answers': correct_answers
    }
