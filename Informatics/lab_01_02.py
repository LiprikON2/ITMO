'''
 Логические операции
'''
f = True
g = False
print("f: ", f)
print("not f: ", not f)
print("f and g: ", f and g)
print("f or g: ", f or g)
print("f == g: ", f == g)
print("f != g: ", f != g)
print("\n")
h = 3
i = 5
print("h = ", h)
print("i = ", i)
print("h > i: ", h > i)
print("h < i: ", h < i)
print("h >= i: ", h >= i)
print("0 < h <= i: ", 0 < h <= i)
print("\n\n")
'''
например:
0 <= h <= 10
Для работы с двоичными представлениями чисел предусмотрены
побитовые операции:
 x & y – побитовое И
 x | y – побитовое ИЛИ
 x ^ y – побитовое исключающее ИЛИ
 ~x – побитовая инверсия числа x
 x >> n – побитовый сдвиг числа x вправо на n бит
 x << n – побитовый сдвиг числа x влево на n бит
Для двоичного представления числового значения используется функция
bin(), при этом число передается в качестве аргумента функции,
например bin(5).
10
 Побитовые операции
'''
j = 7
k = 20
print("j = %d; j in binary format: %s" % (j, bin(j)))
print("k = %d; k in binary format: %s" % (k, bin(k)))
print("j & k: %d; binary: %s" % (j & k, bin(j & k)) )
# побитовое AND
print("j | k: %d; binary: %s" % (j | k, bin(j | k)) )
# побитовое OR
print("j ^ k: %d; binary: %s" % (j ^ k, bin(j ^ k)) )
# побитовое XOR
print("~k: %d; binary: %s" % (~k, bin(~k)) ) #
# инверсия двоичного числа
print("k>>1: %d; binary: %s" % (k>>1, bin(k>>1)) ) #
# сдвиг на один бит вправо
print("k<<1: %d; binary: %s" % (k<<1, bin(k<<1)) ) #
# сдвиг на один бит влево
print("\n\n")




print("My code:")
print("__________\n")

# Задание 9
print("Задание 9")

A = 21
B = 2
C = True
D = False
print("A:", A, "B:", B, "C:", C, "D", D, "\n")


# Задание 10
print("Задание 10")

print("¬(C∧D): ", not (C and D)) 
print("C∧D∨¬(C∧D): ", C and D or not (C and D))
print("¬C∨D: ", not C or D, "\n")


# Задание 11
print("Задание 11")

print("A<=B: ", A<=B)
print("A>B ∨ A==B: ", A>B or A==B)
print("¬(A<B): ", not (A<B), "\n")


# Задание 12
print("Задание 12")

s = 154
p = 6
print ("Decimal:", "s:", s, "p:", p)
print ("Binary:", "s:", bin(s)[2:], "p:", bin(p)[2:], "\n")


# Задание 13
print("Задание 13")
print("s | p - побитовое ИЛИ")
# Применение ИЛИ к каждой паре бит, стоящих на одинаковой позиции

s = s | p
print ("Decimal:", "s:", s)
print ("Binary:", "s:", bin(s)[2:], "\n")


# Задание 14
print("Задание 14")
print("s >> 2, p >> 2 – побитовый сдвиг числа s, p вправо на 2 бит")
# s >> 1 is equvalent to s // 2^1

print('Given: Decimal:', 's:', s, 'p:', p)
print ("Given: Binary:", "s:", bin(s)[2:], "p:", bin(p)[2:], "\n")
s = s >> 2
p = p >> 2
print ("Shift to right: Decimal:", "s:", s, "p:", p)
print ("Shift to right: Binary:", "s:", bin(s)[2:], "p:", bin(p)[2:], "\n")
print("__________\n")