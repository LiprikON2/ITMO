# Converts positive numbers read from file to desired number system
# File must be in following format:
# 10 2 121 13 10 2018 5
# BASE DESIRED_BASE NUM1 NUM2 NUM3

def to_decimal(number: int, base: int):
    new_number = 0
    print('got', number)
    for index, digit in enumerate(str(number)):
        new_number += int(digit) * base**(int(index))
    
    return new_number

def lower_base_of_decimal(number: int, base: int):
    print('Number:', number, 'Base:', base)
    
    number_arr = []
    # Consequential division of number by 14
    while number // base > 0:
        number_arr.append(str(number % base))
        number = number // base
    else:
        number_arr.append(str(number % base))
        
    number_arr.reverse()
    new_number = convert_to_letters(number_arr)
    
    return new_number

def convert_to_letters(number_arr: list) -> str:
    # Change digits to correct symbols
    for i in range(len(number_arr)):
        if number_arr[i] == '10':
            number_arr[i] = 'A'
        if number_arr[i] == '11':
            number_arr[i] = 'B'
        if number_arr[i] == '12':
            number_arr[i] = 'C'
        if number_arr[i] == '13':
            number_arr[i] = 'D'
        if number_arr[i] == '14':
            number_arr[i] = 'E'
        if number_arr[i] == '15':
            number_arr[i] = 'F'
            
    # .lstrip('0') - removes leading zeros
    new_number = ''.join(number_arr).lstrip('0')
    
    return new_number

if __name__ == '__main__':
    line_arr = []
    with open('file.txt') as f:
        for line in f.readlines():
            line = line.strip('\n')
            line_arr.append(line.split(' '))
    
    num1 = to_decimal(int(line_arr[0][2]), 10)
    # num = lower_base_of_decimal(int(line_arr[0][2]), 16)
    print(num1)
