#!/usr/bin/env python
# -*- coding: utf-8 -*-

normalized_leg = {
    "0": "1,0,0,0,0,0", 
    "2": "0,1,0,0,0,0",
    "4": "0,0,1,0,0,0",
    "5": "0,0,0,1,0,0",
    "6": "0,0,0,0,1,0",
    "8": "0,0,0,0,0,1"
}

datafile_in  = "zoo.data"
datafile_out = "zoo_data_norm.txt"

outf = open(datafile_out,"w")

for li in open(datafile_in):
    tmp = li.strip("\n").split(",")
    tmp[0] = "%8s" % tmp[0]
    tmp[13] = normalized_leg[tmp[13]]
    outf.write(",".join(tmp) + "\n")
   
