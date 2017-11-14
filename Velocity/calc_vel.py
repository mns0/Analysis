#!/usr/bin/python

import sys
from math import *



foo = str(sys.argv[1])

binSize = 0.2
binSize = 20
average = 0
avg = 0
count = 0
prevPos = 0
velArr = []


with open(foo) as f:
	for line in f:
		ar = line.split(' ')
		if count == 0:
			prevPos = float(ar[1])
		mod = round(float(ar[0]),2) % binSize
		if mod == 0:
			#print ar[0]
			curPos = float(ar[1])
			dis = curPos - prevPos
			vel = dis / binSize
			velArr.append(vel)
			prevPos = curPos
		count+=1

total = 0
tt = 0
count = 0
for ele in velArr:
	if count != 0:
		total+=abs(ele)
		tt+=ele*ele
	count +=1
#print(velArr)
avgVel = total/ (len(velArr) - 1)
se = sqrt( tt/  (len(velArr) - 1 )  - (total/(len(velArr) -1))**2     ) / (len(velArr) -1 )
sd = sqrt( tt/  (len(velArr) - 1 )  - (total/(len(velArr) -1))**2      )
print(avgVel,sd)
