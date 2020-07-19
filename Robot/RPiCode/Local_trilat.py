# calculate robot position from three points
# input:
    #list of three tuples: (tag number, x-coord, y-coord)
    #list of three tuples: (tag number, range)
#output: x and y in arena coordinates
def Local(coord, rng):
    x1=coord[0][1]
    y1=coord[0][2]
    r1=rng[0][1]
    x2=coord[1][1]
    y2=coord[1][2]
    r2=rng[1][1]
    x3=coord[2][1]
    y3=coord[2][2]
    r3=rng[2][1]
    
    A = 2*x2 - 2*x1
    B = 2*y2 - 2*y1
    C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = 2*x3 - 2*x2
    E = 2*y3 - 2*y2
    F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
    x = (C*E - F*B) / (E*A - B*D)
    y = (C*D - A*F) / (B*D - A*E)    
    return x,y

list = [('t0',0,76), ('t1',50,76), ('t3',100,36)]
rng = [('t0',83),('t1',52),('t3',36)]
x,y = Local(list,rng)
print(x,y)