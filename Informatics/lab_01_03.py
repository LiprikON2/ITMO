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
print("m = %s; pi = %.3f" % (m, pi))

# Задание 17
print("m = {}; pi = {}".format(m[-4:], round(pi, 3)))

# Задание 18
year = input("Год курса обучения: ")
print("\n", year, "г")

# Задание 19
while True:
    try:
        r1, m1, p1 = input("\nВведите ваши баллы ЕГЭ по трем предметам через запятую: ").split(",")
    except ValueError:
        print("Нужно 3 числа через запятую!")
        continue
    else:
        break
    
print("Ваши баллы: {}, {}, {}".format(r1, m1, p1), "\n")
    
# Задание 20
#   Мой день рожденья - (12 % 8) + 2 = 6
number_6 = input("Введите двенадцатиразрядное число в системе счисления 6: ")
number_10 = number_6
for i in range(number_6):
    n = number_6[:]
    



print("__________\n")