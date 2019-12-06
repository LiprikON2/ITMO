# Задание 15
print('Задание 15')

# Input validation
while True:
    number = int(input('Введите шестнадцатеричное число на восемь разрядов: '), 16)
    if (number >= -127) and (number <= 128):
        break
    else:
        print('Введите корректное шестнадцатеричное число на восемь разрядов!')

# Convert decimal to binary string
def dec_to_bin_str(num: int) -> str:
    if num > 0:
        return str(bin(num))[2:]
    else:
        return str(int(str(bin(num))[3:]) * - 1)

# Get two's complement of binary number
def twos_complement(num: str, bits: int = 8) -> int:
    if int(num) < 0:
        # ['-', '1', '0', '1']
        num_arr = list(num)
        
        # Switch minus for zero
        # ['0', '1', '0', '1']
        num_arr[0] = '0'
        
        # Add leading zeros according to number of bits
        # ['0', '0', '0', '0', '0', '1', '0', '1']
        for i in range(bits - len(num_arr)):
            num_arr.insert(1, '0')
        
        # Invert numbers
        for i in range(len(num_arr)):
            if num_arr[i] == '0':
                num_arr[i] = '1'
            elif num_arr[i] == '1':
                num_arr[i] = '0'
        string = ''.join(num_arr)
        
        # Add 1 to the result
        return int(string, 2) + 1
    else:
        return int(num, 2)
    
    
    

number_str = dec_to_bin_str(number)

complement = bin(twos_complement(number_str))

print('Дано (16):', hex(number)[2:])
print('Дано (02):', number_str)

print('Получено (16):', hex(int(complement[2:], 2))[2:])
print('Получено (02):', complement[2:])

# -80 ДОЛЖНО ПОДХОДИТЬ
# [-128,127] для 8 разрядов
# http://hostciti.net/calc/it/inverse-additional-codes.html