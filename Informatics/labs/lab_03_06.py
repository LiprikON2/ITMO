''' 
    Функции 
''' 
def dictUpdate(a): 
    a.update([("x",5)]) 
    print("dict in function: ",a) 
    return 
def dictNoUpdate(a): 
    a = a.copy() 
    a.update([("y",3)]) 
    print("dict in function: ",a) 
    return 
def returnFunc(a): 
    def f1(a): 
        print("returned f1(a): ",a) 
    return f1 
d= {"v":7} 
dictUpdate(d) 
print("dict out of function: ",d) 
dictNoUpdate(d) 
print("dict out of function: ",d) 
f = returnFunc(d) 
print("f: ", f) 
f (2) 
print ("\n")



print("My code:")
print("__________\n")


# Задание 17
print('Задание 17')

def returnMod(a):
    print(a % 15)
    return a % 15

mod15 = returnMod(100)

print("__________\n")