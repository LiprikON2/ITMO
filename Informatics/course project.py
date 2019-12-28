# Converts positive numbers read from file to desired number system
# File must be in following format:
# 10 2 121 13 10 2018 5
# BASE DESIRED_BASE NUM1 NUM2 NUM3

from typing import Any, List


def to_decimal(number: Any, base: int) -> int:
    """ Convert number to decimal number system"""

    digits = [digit for digit in str(number)]
    
    if base > 10:
        digits = convert_to_numbers(digits)

    new_number = 0
    for index, digit in enumerate(digits):

        inversed_index = len(digits) - 1 - index

        new_number += int(digit) * base**(int(inversed_index))

    return new_number


def change_base_of_dec(number: int, desired_base: int) -> str:
    """ Convert decimal to specified number system"""

    numbers = []
    # Consequential division of number by the base
    while number // desired_base > 0:
        numbers.append(str(number % desired_base))
        number = number // desired_base
    else:
        numbers.append(str(number % desired_base))

    numbers.reverse()

    new_number = convert_to_letters(numbers)

    return new_number


def convert_to_letters(digits: List[str]) -> str:
    """ Convert numbers to letters if necessary"""

    for i in range(len(digits)):
        if digits[i] == '10':
            digits[i] = 'A'
        elif digits[i] == '11':
            digits[i] = 'B'
        elif digits[i] == '12':
            digits[i] = 'C'
        elif digits[i] == '13':
            digits[i] = 'D'
        elif digits[i] == '14':
            digits[i] = 'E'
        elif digits[i] == '15':
            digits[i] = 'F'
        elif int(digits[i]) >= 16:
            print('Системы счисления с основанием больше 16 не поддерживаются')
            raise SystemExit()

    # Remove leading zeros
    new_number = ''.join(digits).lstrip('0')

    return new_number


def convert_to_numbers(digits: List[str]) -> List[str]:
    """ Convert letters to digits if necessary"""

    for i in range(len(digits)):
        if digits[i] in 'aA':
            digits[i] = '10'
        elif digits[i] in 'bB':
            digits[i] = '11'
        elif digits[i] in 'cC':
            digits[i] = '12'
        elif digits[i] in 'dD':
            digits[i] = '13'
        elif digits[i] in 'eE':
            digits[i] = '14'
        elif digits[i] in 'fF':
            digits[i] = '15'
        elif digits[i] not in '0123456789':
            print('Системы счисления с основанием больше 16 не поддерживаются')
            raise SystemExit()

    return digits


def handle_lines(lines: List[List[str]]) -> List[str]:

    output = []
    for line in lines:
        given_nums = line[2:7]
        base_of_given_num = int(line[0])
        desired_base = int(line[1])

        print(f'---- ---- {base_of_given_num} => {desired_base} ---- ----')
        for given_num in given_nums:
            decimal = to_decimal(number=given_num, base=base_of_given_num)

            if desired_base == 10:
                desired_num = str(decimal)
            else:
                desired_num = change_base_of_dec(
                    number=decimal, desired_base=desired_base)

            output.append(desired_num)
            print(
                f'{given_num}({base_of_given_num}) => {decimal}(10) => {desired_num}({desired_base})')
        print('\n')
    return output


if __name__ == '__main__':
    # Read numbers from file
    lines = []
    with open('input.txt') as f:
        for line in f.readlines():
            line = line.strip('\n')
            lines.append(line.split(' '))

    handle_lines(lines)