''' 
    Множества 
''' 
# создание множества 
b1 = set() 
print("Set b1 = ", b1) 
b2 = {"bear", "fox", "squirrel", "woodpecker", "woodpecker", "wolf", "hedgehog"} 
print ("Set b2 = ", b2) 
# создание множества из строки 
b3 = set("abcdabcdefg") 
print("Set b3 from string: ", set(b3)) 
print("\n") 





print("My code:")
print("__________\n")


# Задание 6
print('Задание 6')

s = "Electricity is the set of physical phenomena associated with the presence of electric charge. Lightning is one of the most dramatic effects of electricity"
set1 = set(s)
print(set1, '\n')


# Задание 7
print('Задание 7')

arr1 = list(set1)

for i in range(len(arr1)):
    # Check if letter is vowel
    if arr1[i] in "aeiouAEIOU":
        print(arr1[i])
        

print("__________\n")