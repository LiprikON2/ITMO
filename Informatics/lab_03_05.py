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

''' 
    Операции cо словарями 
''' 
d5 = d2.copy() # создание копии словаря 
print("Dict d5 copying d2 = ", d5)
# получение значения по ключу 
print("Get dict value by key d5['bag']: ", d5["bag"]) 
print("Get dict value by key d5.get('bag'): ", d5.get('bag')) 
print("Get dict keys d5.keys(): ", d5.keys()) # список ключей 
print("Get dict values d5.values(): ", d5.values()) # список значений 
print("\n")


print("My code:")
print("__________\n")


# Задание 15
print('Задание 15')

myInfo = {
   'surname': 'Иванов',
   'name': 'Иван',
   'middlename': 'Иванович',
   'day': '2',
   'month': '12',
   'year': '1990',
   'university': 'ITMO'
}

print(myInfo['surname'])
print(myInfo['name'])
print(myInfo['middlename'])
print(myInfo['day'])
print(myInfo['month'])
print(myInfo['year'])
print(myInfo['university'])


print("__________\n")