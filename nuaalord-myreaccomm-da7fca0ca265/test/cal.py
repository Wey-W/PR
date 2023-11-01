import math

x = 4.21
y = 0.34

E = math.exp(x + (y**2)/2)

D = (math.exp(y**2 - 1)) * math.exp(2 * x + y**2)

print(E)


