# Задание 16
print('Задание 16')

number12 = input("Введите двенадцатеричное число: ")

number10 = int(number12, 12)
number14_arr = []

base = 14
# Consequential division of number by 14
while number10 // base > 0:
    number14_arr.append(str(number10 % base))
    number10 = number10 // base
else:
    number14_arr.append(str(number10 % base))
    

# Change digits to correct symbols
for i in range(len(number14_arr)):
    if number14_arr[i] == '10':
        number14_arr[i] = 'A'
    if number14_arr[i] == '11':
        number14_arr[i] = 'B'
    if number14_arr[i] == '12':
        number14_arr[i] = 'C'
        
number14_arr.reverse()

# .lstrip('0') - removes leading zeros
number14 = ''.join(number14_arr).lstrip('0')
print('Число переведено в систему с основанием 14:', number14)