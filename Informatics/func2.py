# Защита 3 лабараторной работы
import random
from pprint import pprint as pp

# Матрица 8х8
DIMS = 8

# matrix = [[random.randint(-1, 9) for i in range(DIMS)] for j in range(DIMS)]
print("Матрица сгенерирована!")
matrix = [[0, -2, 4, 6, 8, 9, 0, 0],
         [-2, 3, 3, 4, 0, 4, 4, 8],
         [4, 6, 2, 1, 0, 4, 4, 7],
         [6, 3, 8, 7, 6, 8, 3, 9],
         [8, 3, 4, 2, 8, 8, 3, 7],
         [9, 2, 4, -8, 0, 8, 5, 4],
         [0, 4, 4, 3, 3, 5, 9, 7],
         [0, 4, 4, 0, 5, 9, 7, 0]]

pp(matrix)

def find_k(matrix):
    # Transpone matrix
    transponed_matrix = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    
    k_arr = []
    for k in range(len(matrix)):
        if matrix[k] == transponed_matrix[k]:
            k_arr.append(k)
    
    if not k_arr:
        k_string = '\n―'
    else:
        k_string = '\n'
        for i in range(len(k_arr)):
            k_string += '{}-ые\n'.format(k_arr[i] + 1)
    
    print('\nСледущие столбцы и строки одинаковы:', k_string)
        

def find_sum(matrix):
    
    col_sum = set()
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] < 0:
                col_sum.add((i, sum(matrix[i])))
    
    # Convert set to list
    col_sum = list(col_sum)
    
    if not col_sum:
        sum_string = '\n―'
    else:
        sum_string = '\n'
        for i in range(len(col_sum)):
            sum_string += '{}-ая строка, с суммой {}\n'.format(col_sum[i][0] + 1, col_sum[i][1])
            
    print('Следущие строки содержащат отрицательные числа:', sum_string)




find_k(matrix)

find_sum(matrix)
