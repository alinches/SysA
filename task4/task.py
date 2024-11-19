from collections import defaultdict
from functools import reduce
from math import log2

def get_event_counts():
    """Вычисление частот появления событий A, B и совместного AB"""
    joint_counts = {}
    sum_counts = {}
    product_counts = {}
    
    for dice1 in range(1, 7):
        for dice2 in range(1, 7):
            dice_sum = dice1 + dice2
            dice_product = dice1 * dice2
            
            joint_counts[(dice_sum, dice_product)] = joint_counts.get((dice_sum, dice_product), 0) + 1
            sum_counts[dice_sum] = sum_counts.get(dice_sum, 0) + 1
            product_counts[dice_product] = product_counts.get(dice_product, 0) + 1

    return joint_counts, sum_counts, product_counts

def convert_to_probabilities(counts, total_outcomes):
    """Преобразование частот в вероятности"""
    
return {key: value / total_outcomes for key, value in counts.items()}


def calculate_entropy(probabilities):
    """Вычисление энтропии Шеннона."""
    entropy = 0
    for prob in probabilities.values():
        if prob > 0:
            entropy -= prob * log2(prob)
    return entropy


def calculate_results():
    total_outcomes = 36  # Общее количество исходов при броске двух кубиков

    # Получение частот событий
    joint_counts, sum_counts, product_counts = get_event_counts()

    # Преобразование частот в вероятности
    joint_probabilities = convert_to_probabilities(joint_counts, total_outcomes)
    sum_probabilities = convert_to_probabilities(sum_counts, total_outcomes)
    product_probabilities = convert_to_probabilities(product_counts, total_outcomes)

    # Вычисление энтропий
    entropy_joint = calculate_entropy(joint_probabilities)  
    entropy_sum = calculate_entropy(sum_probabilities)      
    entropy_product = calculate_entropy(product_probabilities)  

    # Условная энтропия и информация
    conditional_entropy = entropy_joint - entropy_sum  
    mutual_information = entropy_product - conditional_entropy  

    # Возвращение округленных значений
    return [
        round(entropy_joint, 2),
        round(entropy_sum, 2),
        round(entropy_product, 2),
        round(conditional_entropy, 2),
        round(mutual_information, 2),
    ]


if __name__ == '__main__':
    print(calculate_results())
