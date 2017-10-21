#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

def nonline(x, deriv=False):
    if (deriv == True):
        return x * (1 - x)
    return 1.0 / (1 + np.exp(-x))

X = np.array([  [0,1,1,1,0],
                [0,1,1,1,0],
                [1,0,1,1,0],
                [1,1,1,1,0] ])

y = np.array([[0,0,1,1]]).T

def load_softset():
    xset = []
    for li in open("FA.txt"):
        ls = li.strip("\n").split(",")
        ls = [int(c)  for c in ls]
        xset.append(ls)
    return xset

def load_mux():
    yset = []
    for li in open("mux.txt"):
        ls = li.strip("\n").split(",")
        ls = [int(c) for c in ls]
        yset.append(ls)
    return yset

#X = np.array(load_softset())
#y = np.array(load_mux()).T

pos = 0
xset = []
yset = []
for li in open("zoo.txt"):
    pos+=1
    ls = li.strip("\n").split(",")
    print ls
    if pos > 30:
        break

    x1 = ls[1:-1]
    x1 = [int(c)  for c in x1]
    x1[12] = x1[12]
    xset.append(x1)
    y1 = int(ls[-1]) / 10.0
    yset.append(y1)

print xset
print yset
    
X = np.array(xset)
y = np.array([yset]).T

np.random.seed(1)

attribute_number = len(X[0])
object_number = len(X) 
output_node = 1
print "object_number", object_number

syn0 = 2 * np.random.random((attribute_number,object_number)) - 1
syn1 = 2 * np.random.random((object_number,output_node)) - 1

for it in range(0, 10000):
    L0 = X 
    L1 =  nonline(np.dot(L0, syn0))
    L2 =  nonline(np.dot(L1, syn1))

    l2_error = y - L2
    l2_delta = l2_error * nonline(L2, deriv=True)
    #print "L1->",L1
    #L1_error = y - L1
    l1_error = l2_delta.dot(syn1.T)
    # print "L1_er->",l1_error

    l1_delta = l1_error * nonline(L1, True)

    syn1 += L1.T.dot(l2_delta)
    syn0 += L0.T.dot(l1_delta)
    #print "syn0->",syn0


#x = [1,0,1,1,0,1,0,1]
def think(v):
    l1 = nonline(np.dot(v, syn0))
    X = np.dot(l1,syn1)
    l2 = nonline((X))
    return l2

#print think(x)
#print "syn0", syn0
#print "syn1", syn1

pos = 0
for li in open("zoo.txt"):
    te = li.strip("\n").split(",")
    anity = int(te[-1]) / 10.0
    x1 = te[1:-1]
    x1 = [int(c) for c in x1]
    x1[12] = x1[12] 
    thk = think(x1)
    if abs(thk - anity) > 0.1:
        pos += 1
        print li,thk,"------------------"
print pos
