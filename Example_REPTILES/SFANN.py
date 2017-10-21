#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import sys

ANIMAL_TYPE = 3
TOTAL_ANIMAL_NUMBER = 5

def Ysigmoid(x):
    return 1.0 / (1 + np.exp(-x))

def Ysigmoid_deriv(x):
    return x * (1 - x)

def print_matrix(x):
    for i in x:
        print i 

def load_training_set(filenm, animal_type):
    softset  = []
    fuzzyset = []
    for li in open(filenm):
        tmp = li.strip("\n").split(",")
        x1 = tmp[1:-1]
        x1 = [int(c)  for c in x1]
        softset.append(x1)

        if animal_type == int(tmp[-1]):
            fuzzyset.append(1)
        else:
            fuzzyset.append(0)
    return softset, fuzzyset

def trainning_sfann(softset, fuzzyset):
    softset  = np.array(softset)
    fuzzyset = np.array([fuzzyset]).T

    attribute_number = len(softset[0])

    # hide layer nodes
    object_number    = 8 

    output_node      = 1

    np.random.seed(1)
    w1 = 2 * np.random.random((attribute_number,object_number)) - 1
    w2 = 2 * np.random.random((object_number,output_node)) - 1
    
    for it in range(0, 1000):
        layer0 =  softset 
        layer1 =  Ysigmoid(np.dot(layer0, w1))
        layer2 =  Ysigmoid(np.dot(layer1, w2))
    
        layer2_error = fuzzyset - layer2
        layer2_delta = layer2_error * Ysigmoid_deriv(layer2)

        layer1_error = layer2_delta.dot(w2.T)
        layer1_delta = layer1_error * Ysigmoid_deriv(layer1)
    
        w2 += layer1.T.dot(layer2_delta)
        w1 += layer0.T.dot(layer1_delta)

    return w1,w2

def think(v, w1, w2):
    return Ysigmoid(np.dot(Ysigmoid(np.dot(v, w1)), w2))


def test_sfann(testsetname, w1, w2, animal_type):
    """
    Total:41
    1 (41) aardvark, antelope, bear, boar, buffalo, calf,
                 cavy, cheetah, deer, dolphin, elephant,
                 fruitbat, giraffe, girl, goat, gorilla, hamster,
                 hare, leopard, lion, lynx, mink, mole, mongoose,
                 opossum, oryx, platypus, polecat, pony,
                 porpoise, puma, pussycat, raccoon, reindeer,
                 seal, sealion, squirrel, vampire, vole, wallaby,wolf
    Number of Instances: 101
    """
    total_num = TOTAL_ANIMAL_NUMBER

    find_num  = 0
    error_num = 0
    correct_num = 0
    identif_msg = ""
    for li in open(testsetname):
        temp = li.strip("\n").split(",")
        ani_type = int(temp[-1])
        softset_obj = temp[1:-1]
        softset_obj = [int(c) for c in softset_obj]
        mux = think(softset_obj, w1, w2)
        if mux > 0.9:
            find_num += 1
            if ani_type == animal_type:
                correct_num += 1
                identif_msg = "OK"
            else:
                error_num += 1
                identif_msg = "FAIL"
            
            print li.strip("\n"), "\t", "mux=%.5f DesireOutput:%d  Output:%d  %s" % \
                (mux, animal_type, ani_type, identif_msg)
    print "Total number: %d" % total_num 
    print "Find  numper: %d" % find_num
    print "Error numper: %d" % error_num
    print "Corre number: %d" % correct_num

    accurt = (correct_num * 1.0) / find_num
    recall = (correct_num * 1.0) / total_num
    f1 = accurt * recall * 2 / (accurt + recall)

    print "PRECISION:%.3f  RECALL:%.3f  F1-SCORE:%.3f" % (accurt, recall, f1)

if __name__ == '__main__':
    filenm = "training.txt"
    animal_type = ANIMAL_TYPE
    softset, fuzzyset = load_training_set(filenm, animal_type)
    print "Softset ==>"
    print_matrix(softset)

    print "Fuzzyset ==>"
    print fuzzyset

    w1,w2 = trainning_sfann(softset, fuzzyset)
    print "W1==>\n", w1
    print "W2==>\n", w2
    test_sfann("test.txt", w1, w2, animal_type)

    sys.exit(0)

