# -*- coding: utf-8 -*-
#多线程版
#求两个点之间的欧几里得距离
#输入a和b是含有点坐标的列表
import threading
from math import sqrt

#全局变量X,mutex
X=[]
mutex=threading.Lock()

def EucliDis(a,b):
   return sqrt(sum([pow(a[i]-b[i],2) for i in range(len(a))]))
   
#求两个轮廓线之间的Hausdorff Distance
#对于A中的每一个点，求该点与B中所有点的欧几里得距离，取最小值
#然后在A中的所有点中，取最大值
def HausDis2(a,b):
    global X,mutex
    t1=[]
    for i in range(len(a)):
        t2=[]
        for j in range(len(b)):
            t2.append(EucliDis(a[i],b[j]))
        t1.append(min(t2))
    #取得锁
    mutex.acquire()
    X.append(max(t1))
    #释放锁
    mutex.release()

    
#多进程运算
def HausDis(a,b):
    global X,mutex
    X=[]
    #创建一个锁
    mutex=threading.Lock()
    #创建两个线程
    t1=threading.Thread(target=HausDis2,args=(a,b,))
    t2=threading.Thread(target=HausDis2,args=(b,a,))
    #启动所有线程
    t1.start()
    t2.start()

    #主线程等待所有子线程退出
    t1.join()
    t2.join()
 
    return max(X)