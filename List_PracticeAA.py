# playpen to familiarize myself with handling 2-D lists efficiently
# Ctrl + / to comment or uncomment
import math
from operator import itemgetter
import csv

# lists:
#       tags (4) on the top of robots (probably input from .csv file)
#               tagnr
#               robotID
#               tagpos (0-bow, 1-starboard, 2-stern, 3-port)
#       tags detected by the three cameras
#               tagnr
#               rng (range from camera to tag)
#               cameraID
print('read and print csv')
with open('robot_tags.csv', 'r') as file:
    next(file,None)    # skip header row
    reader = csv.reader(file)
    data = list(reader)
    print('data as string')
    for r in data:
        print(r)
for ri in range(len(data)):
        data[ri][0] = int(data[ri][0])
        data[ri][1] = int(data[ri][1])
        data[ri][2] = int(data[ri][2])
print('data as int')
for r in data:
        print(r)



rtags = [
        [0, 1, 0],
        [1, 1, 1],
        [2, 1, 2],
        [3, 1, 3],
        [10, 2, 0],
        [11, 2, 1],
        [12, 2, 2],
        [13, 2, 3],
        [20, 3, 0],
        [21, 3, 1],
        [22, 3, 2],
        [23, 3, 3]
]
ctags = [
        [10, 99, 1],
        [11, 70, 2],
        [12, 71, 2],
        [13, 50, 3],
        [23, 60, 2],
        [22, 64, 3],
        [20, 45, 1],
        [21, 44, 1]
]
for rw in rtags:
        print(rw)

#rtags = sorted(rtags, key=lambda robotID: robotID[2])
print('rtags: ',rtags)
for rw in rtags:
        print(rw)
for rw in ctags:
        print(rw)
print('ctags: ',ctags)
det = [] #list of detected targets by the three cameras
detsorted = []
tup = []
ctlen = len(ctags)
rtlen = len(rtags)
print('ctlen: ',ctlen, ' rtlen: ',rtlen)
for i in range(ctlen):
        for j in range(rtlen):
                if ctags[i][0] == rtags[j][0]:
                        print('camera {} detected tag {} on robot {}'.
                              format(ctags[i][2],ctags[i][0],rtags[j][1]))
                        #append the robot ID, tag num and range to the detected list
                        # tup[0] = rtags[j][1]
                        # tup[1] = ctags[i][0]
                        # tup[2] = ctags[i][1]
                        det.append([rtags[j][1],ctags[i][0],ctags[i][1]])
                        print('det: ', det)
                        for rw in det:
                                print(rw)
print('list to sort: ',det)
det = sorted(det, key=lambda robotID: robotID[0])
#det.sort(key=lambda robotID: robotID[0])
#det.sort(key=itemgetter(0))
print('after sort')
print('detsorted: ',det)

