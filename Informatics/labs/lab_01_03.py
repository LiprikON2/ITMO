'''
 Форматированный ввод/вывод данных
'''
m = 10
pi = 3.1415927
print("m = ",m)
print("m = %d" % m)
print("%7d" % m)
print("pi = ", pi)
print("%.3f" % pi)
print("%10.4f\n" % pi)
print("m = {}, pi = {}".format(m,pi))
ch = 'A'
print("ch = %c" % ch)
s = "Hello"
print("s = %s" % s)
print("\n\n")
code = input("Enter your position number in group: ")
n1, n2 = input("Enter two numbers splitted by space: ").split()
d, m, y = input("Enter three numbers splitted by\'.\': ").split('.')
print("{} + {} = {}".format(n1,n2,float(n1)+float(n2)))
print("Your birthday is %s.%s.%s and you are %d in the group list" % (d,m,y,int(code)) )



print("\nMy code:")
print("__________\n")

# Задание 16
print("Задание 16")

print("m = %4d; pi = %.3f" % (int(m), pi), "\n")


# Задание 17
print("Задание 17")

print("m = {}; pi = {}".format(m, pi), "\n")


# Задание 18
print("Задание 18")

year = input("Год курса обучения: ")
print("Вы ввели:", year,"год обучения", "\n")


# Задание 19
print("Задание 19")

while True:
    try:
        r1, m1, p1 = input("Введите ваши баллы ЕГЭ по русскому, математике и профильному предмету через запятую: ").split(",")
    except ValueError:
        print("Нужно 3 числа через запятую!")
        continue
    else:
        break

print("Ваши баллы: {}, {}, {}".format(r1, m1, p1), "\n")
    

# Задание 20
print("Задание 20")

print("Мой день рожденья: (12 mod 8) + 2 = 6")
given_num = input("Введите двенадцатиразрядное число в системе счисления 6: ")

# Convert given_num to string and reverse the order
num_str = str(given_num)[::-1]
# Determine number of digits in given number
digits = len(num_str)

base = 6
num_10 = 0
for n in range(digits):
    if not num_str[n] == '-':
        if int(num_str[n]) < 6:
            num_10 += int(num_str[n]) * base**n
        else:
            raise ValueError("Было введено некорректное число!")
    else:
        num_10 *= -1

print(given_num, "в десятичной:", num_10, "\n")


# Задание 21
print("Задание 21")
# s >> 1 is equvalent to s // 2^1
# s << 1 is equvalent to s * 2^1

number = int(input("Введите число, чтобы осуществить умножение и деление с использованием операции побитого сдвига влево и вправо соответственно: "))
print("Умножение:", number << 1, "Деление:", number >> 1)

print("__________\n")