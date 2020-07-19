# 101computing.net/cell-phone-trilateration-algorithm
x1=0
y1=76
r1=83
x2=50
y2=76
r2=52
x3=100
y3=36
r3=36

A = 2*x2 - 2*x1
B = 2*y2 - 2*y1
C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
D = 2*x3 - 2*x2
E = 2*y3 - 2*y2
F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
x = (C*E - F*B) / (E*A - B*D)
y = (C*D - A*F) / (B*D - A*E)
print(x,y)