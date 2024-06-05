import numpy as np

def correlation_between_even_odd(matrix):
    even_indices = matrix[::2]  # Чётные индексы
    odd_indices = matrix[1::2]  # Нечётные индексы

    even_mean = np.mean(even_indices)
    odd_mean = np.mean(odd_indices)

    cov = np.sum((even_indices - even_mean) * (odd_indices - odd_mean))
    correlation = cov / (len(even_indices) - 1)

    return correlation

# Пример использования
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9],
                   [10, 11, 12]])

result = correlation_between_even_odd(matrix)
print("Коэффициент корреляции:", result)