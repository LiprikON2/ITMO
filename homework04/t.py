from string import ascii_lowercase


a = ord('а')
rus_lowercase = ''.join([chr(i) for i in range(a,a+6)] + [chr(a+33)] + [chr(i) for i in range(a+6,a+32)])


letters = set()
for c in ascii_lowercase:
    letters.add(c)
for c in rus_lowercase:
    letters.add(c)
    
    

print(letters)

# letters.add(list(s))
# for i in range(ord("a"), ord("z") + 1):
#     letters.update(chr(i))
# for i in range(ord("а"), ord("я") + 1):
#     letters.update(chr(i))
