import sys

if hasattr(sys, 'real_prefix'):
    print("venv is online!")
print("Hello world!")
print(sys.real_prefix)
print("Hello world!")
   
