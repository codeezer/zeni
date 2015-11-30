#!/usr/bin/env python
# -*- coding: utf-8 -*-

def coeff(word = []):
    n1 = len(word[0]);
    n2 = len(word[1]);
    intersection =  min(n1,n2);
    union = n1+n2;
    coeff = intersection/union;
    return coeff

kaka=[]
kaka.append(['potat','poapptto'])
kaka.append(['potat','tomato'])
kaka.append(['potat','potuu'])
n=[]
n.append(coeff(kaka[0]));
n.append(coeff(kaka[1]));
n.append(coeff(kaka[2]));
m = max(n)
p = [i for i, j in enumerate(n) if j == m]

print(kaka[p[0]][0]+" ?? Did you mean :"+kaka[p[0]][1])

