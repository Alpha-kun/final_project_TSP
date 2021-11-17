#!/usr/bin/env python
# coding: utf-8

import sys
import gurobipy as gp
from gurobipy import GRB
import numpy as np


def read_txt(path):
    end1 = []
    end2 = []
    weight = []
    
    with open(path, "r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.split()
            
            if len(line)==2:
                n = line[0]
                m = line[1]
            if len(line)==3:
                end1_tmp = line[0]
                end2_tmp = line[1]
                weight_tmp = line[2]
                
                end1.append(end1_tmp)
                end2.append(end2_tmp)
                weight.append(weight_tmp)
    return n, m, end1, end2, weight
    

def adjacency_matrix(n, m, end1, end2, weight):
    n = int(n)
    m = int(m)
    
    A = np.zeros((n,n))
    
    for i in range(m):
        A[int(end1[i])][int(end2[i])] = int(weight[i])
        A[int(end2[i])][int(end1[i])] = int(weight[i])
    
    return A
