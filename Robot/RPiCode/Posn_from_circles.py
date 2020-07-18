# calculate robot position from intersecting circles
# 17 Jul 2020

import math

Ax, Ay = 0, 76  # center of circle A
Bx, By = 50, 76  # center of cirlce B
Cx, Cy = 100, 76  # center of circle C 
RA, RB, RC = 83, 52, 62 # radius of circles (range from robot)

tagc = [(0,76),(50,76),(100,76)]
rng = [83,52,62]

D = []
delta = []
x1 = []
x2 = []
y1 = []
y2 = []
c1 = 0
c2 = 0
for i in range(len(tagc)):
    c1 = c1 + 1
    print('\n','D calc; i-loop: ', c1)
    for j in range (i+1, len(tagc)):
        c2 = c2 + 1
        print('\n','D calc; j-loop: ',c2)
#        print(tagc[i], tagc[j])
        print('Ax: ', tagc[i][0],' Bx: ', tagc[j][0])
        print('Ay: ', tagc[i][1], ' Bx ', tagc[j][1])
        D.append(math.sqrt(((tagc[i][0] - tagc[j][0])**2) + (tagc[i][1] - tagc[j][1])**2))
        print('\n',"List of d's: ",D)

c1 = 0
c2 = 0
ln=len(D)-1
for i in range(ln):
    c1 = i
    print('\n','i-loop: ', c1)
    for j in range (i+1, len(tagc)):
        c2 = j
        print('\n','i-loop, j-loop: ',c1,c2)
        df1 = D[j-i-1]+rng[i]+rng[j]
        df2 = D[j-i-1]+rng[i]-rng[j]
        df3 = D[j-i-1]-rng[i]+rng[j]
        df4 = -D[j-i-1]+rng[i]+rng[j]
        print('\n','D[j-i], rng[i], rng[j]: ', D[j-i-1], rng[i], rng[j])
        print('\n', 'dfactors: ', df1, df2, df3, df4)
        delta.append(0.25*math.sqrt(df1*df2*df3*df4))
        print('\n','list of deltas: ', delta, '\n')
        f1 = (tagc[i][0] + tagc[j][0])/2
        print('\n','i:',i,'j:',j,' f1: ', f1, ' tagc[i]:',tagc[i][0],' tagc[j]:',tagc[j][0])
        f2 = (tagc[j][0] - tagc[i][0])*(rng[i]**2 - rng[j]**2)/(2*D[j-i-1]**2)
        print('\n','i:',i,'j:',j,'f2: ',f2)
        print('tagc[j]:',tagc[j][0],'tagc[i]:',tagc[i][0],'rng[i]:',rng[i],'rng[j]',rng[j],'D[j-i-1]:',D[j-i-1])
        f3 = (2*(tagc[i][1]-tagc[j][1])/D[j-i-1]**2)*delta[j-i-1]
        print('\n','i:',i,'j:',j,'f3: ',f3)
        print('tagc[i]:',tagc[i][1],'tagc[j]:',tagc[j][1],'D[j-i-1]:',D[j-i-1],'delta[j-i-1]:',delta[j-i-1])
        x1.append(f1 + f2 + f3)           
        print('\n','x1: ', x1)
        x2.append(f1 + f2 - f3)
        print('x2: ', x2)
        g1 = (tagc[i][1] + tagc[j][1])/2
        print('\n','g1: ', g1)
        g2 = (tagc[j][1] - tagc[i][1])*(rng[1]**2 - rng[j]**2)/(2*D[j-i-1]**2)
        print('\n','g2: ',g2)
        g3 = (2*(tagc[i][0]-tagc[j][0])/(D[j-i-1]**2))*delta[j-i-1]
        print('\n','g3: ',g3,' tagc[i]: ',tagc[i][0], ' tagc[j]: ', tagc[j][0], ' D[j-i-1]: ', D[j-i-1], ' delta: ',delta[j-i-1])
        y1.append(g1 + g2 -g3)
        print('\n','y1: ', y1)
        y2.append(g1 + g2 +g3)
        print('y2: ', y2)
        
       
           
#    print('i: ', tagc[ln])
#     for j in tagc[1:]:
#         
#         print('j: ', j)

# D_AB = math.sqrt((Bx-Ax)**2 + (By-Ay)**2)
# print(D_AB)
# delta_AB = .25*math.sqrt((D_AB+RA+RB)*(D_AB+RA-RB)*(D_AB-RA+RB)*(-D_AB+RA+RB))
# print(delta_AB)
# x1 = (Ax+Bx)/2 + ((Bx-Ax)*(RA**2 - RB**2)/(2*D_AB**2)) + 2*((Ay-By)/D_AB**2)*delta_AB
# print('\n', 'x1: ',x1)
# x2 = (Ax+Bx)/2 + ((Bx-Ax)*(RA**2 - RB**2)/(2*D_AB**2)) - 2*((Ay-By)/D_AB**2)*delta_AB
# print('\n', 'x2: ',x2)
# y1 = (Ay+By)/2 + ((By-Ay)*(RA**2 - RB**2)/(2*D_AB**2)) - 2*((Ax-Bx)/D_AB**2)*delta_AB
# print('\n', 'y1: ',y1)
# y2 = (Ay+By)/2 + ((By-Ay)*(RA**2 - RB**2)/(2*D_AB**2)) + 2*((Ax-Bx)/D_AB**2)*delta_AB
# print('\n', 'y2: ',y2)
