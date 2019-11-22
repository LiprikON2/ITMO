''' 
    Циклы 
''' 
# while 
print("Numbers < 10 (while):") 
i = 0 
while (i<10): 
    print(i, end=" ") # print in one line 
    i += 1 
print("\n")
# for 
print("Numbers < 10 (for):") 
for i in range(0,10): 
    print(i, end=" ") 
else: 
    print("\nThe next number is 10\n") 
 
# break 
sum = 0 
for i in range(0,100): 
    if i > 10: 
        print("\nWe reached the end, final sum: ", sum) 
        break 
    sum += i 
 
# continue 
i = 0 
while i<=15: 
    if i % 3 == 0: 
        i += 1 
        continue 
    print(i, end=" ") 
    i += 1
 
print("\n") 
 
# pass 
print("Let's print numbers again!") 
for i in range(0,10): 
    pass 
    print(i, end=" ") 
 
print ("\n\n")







print("My code:")
print("__________\n")

# Задание 5
print('Задание 5')

for i in range(0, 500, 7):
    print(i)
else:
    print('All numbers were printed!\n')
    

i = 0
print('\n')

while i <= 500:
    print(i)
    i += 7
else:
    print('All numbers were printed!\n')
    
    
# Задание 6
print('Задание 6')

for i in range(0, 500, 7):
    if i >= 300:
        break
    if i % 14 != 0:
        print(i)
else:
    print('All numbers were printed!\n')
        
i = 0
print('\n')
while i <= 500:
    if i >= 300:
        break
    if i % 14 != 0:
        print(i)
    i += 7
else:
    print('All numbers were printed!\n')
    
print('\n')
    

# Задание 7
print('Задание 7')

for i in range(1, 5):
    for j in range(1, 5):
        if i == j:
            print(i, end=" ")
        else:
            print('0', end=" ")
    print('\n')
            
print("__________")