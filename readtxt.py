#!/usr/bin/env python
# coding: utf-8

import numpy as np


def read_txt(path):
    end1 = []
    end2 = []
    weight = []

    with open(path, "r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.split()

            if len(line) == 2:
                n = int(line[0])
                m = int(line[1])
            if len(line) == 3:
                end1_tmp = int(line[0])
                end2_tmp = int(line[1])
                weight_tmp = int(line[2])

                end1.append(end1_tmp)
                end2.append(end2_tmp)
                weight.append(weight_tmp)

    A = np.zeros((n, n))

    for i in range(m):
        A[end1[i]][end2[i]] = weight[i]
        A[end2[i]][end1[i]] = weight[i]

    return A