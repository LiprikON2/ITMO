# Защита 2 лабараторной работы

import math

def func(x):
    if x < -4:
        return -2
    elif x >= -4 and x < 0:
        return x / 4
    elif x >= 0 and x <= 2:
        return x**2
    else:
        y = 0.5 * (10 - x)
        if math.ceil(y) == y:
            return int(y)
        else: 
            return y


print('┏━━━━━━━┳━━━━━━━┓')
print('┃   X   ┃   Y   ┃')
print('┣━━━━━━━╋━━━━━━━┫')

for x in range(-13, 14, 1):
    x_str = '{: >5}'.format(x)
    y_str = '{: >5}'.format(func(x))
    print('┃', x_str, '┃', y_str, '┃')
    
print('┗━━━━━━━┻━━━━━━━┛')