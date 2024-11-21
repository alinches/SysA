import json
import numpy as np

def create_relation_matrix(ranking_json: str):
    """Создает матрицу отношений из ранжирования."""
    ranking_groups = [group if isinstance(group, list) else [group] for group in json.loads(ranking_json)]
    size = sum(len(group) for group in ranking_groups)
    # Создание базовой матрицы отношений
    relation_matrix = [[1] * size for _ in range(size)]
    
    previous_elements = []
    for group in ranking_groups:
        for prev_elem in previous_elements:
            for curr_elem in group:
                relation_matrix[curr_elem - 1][prev_elem - 1] = 0
        for elem in group:
            previous_elements.append(int(elem))

    return np.array(relation_matrix)

def determine_clusters(relation_matrix, matrix_a, matrix_b):
    """Определяет кластеры на основе матрицы отношений."""
    clusters = {}
    total_rows = len(relation_matrix)
    processed_rows = set()

    # Объединение элементов в кластеры
    for row in range(total_rows):
        if row + 1 in processed_rows:
            continue
        new_cluster = [row + 1]
        clusters[row + 1] = new_cluster
        for col in range(row + 1, total_rows):
            if relation_matrix[row][col] == 0:
                new_cluster.append(col + 1)
                processed_rows.add(col + 1)

    # Формирование итогового списка кластеров
    final_clusters = []
    for key in clusters:
        if not final_clusters:
            final_clusters.append(clusters[key])
            continue
            
        for i, cluster in enumerate(final_clusters):
            sum_a_cluster = np.sum(matrix_a[cluster[0] - 1])
            sum_b_cluster = np.sum(matrix_b[cluster[0] - 1])
            sum_a_key = np.sum(matrix_a[key - 1])
            sum_b_key = np.sum(matrix_b[key - 1])

            if sum_a_cluster == sum_a_key and sum_b_cluster == sum_b_key:
                for member in clusters[key]:
                    final_clusters[i].append(member)
                    break
            elif sum_a_cluster < sum_a_key or sum_b_cluster < sum_b_key:
                final_clusters = final_clusters[:i] + clusters[key] + final_clusters[i:]
                break

        final_clusters.append(clusters[key])

    return [cluster[0] if len(cluster) == 1 else cluster for cluster in final_clusters]

def task():
    """Основная функция для обработки ранжирования."""
    ranking_a = '[1,[2,3],4,[5,6,7],8,9,10]'
    ranking_b = '[[1,2],[3,4,5],6,7,9,[8,10]]'

    matrix_a = create_relation_matrix(ranking_a)
    matrix_b = create_relation_matrix(ranking_b)

    # Пересечение и объединение матриц
    combined_matrix = np.multiply(matrix_a, matrix_b)
    combined_transposed = np.multiply(np.transpose(matrix_a), np.transpose(matrix_b))
    merged_matrix = np.maximum(combined_matrix, combined_transposed)

    # Определение кластеров
    result_clusters = determine_clusters(merged_matrix, matrix_a, matrix_b)
    return json.dumps(result_clusters)

if __name__ == "__main__":
    print(task())

