# -*- coding: utf-8 -*-
#求两个点之间的欧几里得距离
#输入a和b是含有点坐标的列表
from math import sqrt
def EucliDis(a,b):
   return sqrt(sum([pow(a[i]-b[i],2) for i in range(len(a))]))
   
#求两个轮廓线之间的Hausdorff Distance
#对于A中的每一个点，求该点与B中所有点的欧几里得距离，取最小值
#然后在A中的所有点中，取最大值
def HausDis(a,b):
    t1=[]
    for i in range(len(a)):
        t2=[]
        for j in range(len(b)):
            t2.append(EucliDis(a[i],b[j]))
        t1.append(min(t2))
    t1max=max(t1)
    #求B
    t1=[]
    for i in range(len(b)):
        t2=[]
        for j in range(len(a)):
            t2.append(EucliDis(b[i],a[j]))
        t1.append(min(t2))
    t2max=max(t1)
    #最后取最大值
    return max(t1max,t2max)
        
        