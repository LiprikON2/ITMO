# Задание 14
print('Задание 14')

s = list(input("Введите строку: "))

arr = []

for i in range(len(s)):
    for j in range(len(s) - 1):
        s[j], s[j + 1] = s[j + 1], s[j]
        arr.append(''.join(s))
        
arr = set(arr)
print(arr, '\nПолучилось', len(arr), 'уникальных перестановок, составленных из данной строки')
