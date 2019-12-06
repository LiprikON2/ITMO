''' 
    Словари 
''' 
d1 = { 
    "day": 18, 
    "month": 6, 
    "year": 1983 
} 
d2 = dict(bananas=3,apples=5,oranges=2,bag="basket") 
d3 = dict([("street","Kronverksky pr."), ("house", 49)]) 
d4 = dict.fromkeys(["1","2"], 3) 
print("Dict d1 = ", d1) 
print("Dict d2 by dict()= ", d2) 
print("Dict d3 by dict([])= ", d3) 
print("Dict d4 by fromkeys = ", d4) 
print("\n")



print("My code:")
print("__________\n")


# Задание 12
print('Задание 12')

startDict1 = {
    'ready': 3,
    'set': 2,
    'go': 1,
}
print(startDict1)

startDict2 = dict(ready = 3, set = 2, go = 1)
print(startDict2)

startDict3 = dict.fromkeys(['ready', 'set', 'go'], 1)
print(startDict3, '\n')


# Задание 13
print('Задание 13')

dict1 = dict.fromkeys(['key1', 'key2'], input("Введите значение для key1 и key2: "))

print(dict1)


print("__________\n")