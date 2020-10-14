# -*- coding: utf-8 -*-
#求取指定两个轮廓线的Hausdorff distance
#从Raystation中运行,否则无法连接至Raystation
#----------------------------------------------------------------#
from time import time
from connect import *
from math import sqrt
import threading

#----------------------------------------------------------------#
#求两个点之间的欧几里得距离
#输入a和b是含有点坐标的列表

def EucliDis(a,b):
   return sqrt(sum([pow(a[i]-b[i],2) for i in range(len(a))]))
#----------------------------------------------------------------#
#求两个轮廓线之间的Hausdorff Distance
#对于A中的每一个点，求该点与B中所有点的欧几里得距离，取最小值
#然后在A中的所有点中，取最大值
'''def HausDis(a,b):
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
    return max(t1max,t2max)'''

#多线程版
#全局变量X,mutex
X=[]
mutex=threading.Lock()

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
#-----------------------------------------------------------------# 
#根据ROI类型，获取ROI的点坐标
def RoiCoord(structure_set,x):
    #每一序列下有多个ROIGeometries，可用RoiGeometries[0],[1]或RoiGeometries['ROI名']访问具体的一个ROI
    roi_geometries=structure_set.RoiGeometries[x]
#Contours中包含有组成该ROI轮廓线的所有点坐标（DICOM格式）
#指定Contours的长度len为其所含的CT层数，类型为list，可用Contours[0],[1]访问
#每一层CT指定轮廓线Contours[0]的长度len为点的数目，可用Contours[0][0],[0][1]访问
#每一个点长度len为3，用Contours[0][0].x,y,z来分别获取坐标
    c1=[]
    if hasattr(roi_geometries.PrimaryShape,'Contours'):
        #ROI的类型为Contours
        contour=roi_geometries.PrimaryShape.Contours
        #记录所有点的坐标，结果为一列表
        for i in range(len(contour)):
            for j in range(len(contour[i])):
                c1.append([contour[i][j].x,contour[i][j].y,contour[i][j].z])
    elif hasattr(roi_geometries.PrimaryShape,'Vertices'):
        #ROI的类型为Triangle mesh
        #Vertices中存放点坐标
        contour=roi_geometries.PrimaryShape.Vertices
        #指定ROI的长度len为其所含的点数，类型为list，可用Vertices[0],[1]访问
        #每一个点长度len为3，用Vertices[0].x,y,z来分别获取坐标
        for i in range(len(contour)):
            c1.append([contour[i].x,contour[i].y,contour[i].z])
    else:
        print 'type of ROI is not matched'
    return c1
#----------------------------------------------------------------------------#       
#主程序
def main(x='circle',y='circle2'):
    start=time()
#patient获取为当前患者
    patient=get_current('Patient')

#examination获取为当前CT序列，CT序列名称在属性Name中，一次只能获取一个CT序列
    examination=get_current('Examination')

#StructureSets与CT序列对应，可用object[0],[1],[2]或object['序列名']访问具体的一组Structure
    structure_set=patient.PatientModel.StructureSets[examination.Name]

#内置求距离的两个ROI名称，在Raystation运行中无法用raw_input获取键盘输入
#ROI的类型必须为Contour或者mesh，否则报错
    
#获取点坐标
    c1=RoiCoord(structure_set,x)
    c2=RoiCoord(structure_set,y)
#求Hausdorff Distance并输出
    print 'the name of current patient is:'+patient.PatientName
    print 'the name of current examination is:'+examination.Name
    print 'the Hausdorff Distance between '+x+' and '+y+' is:'+str(round(HausDis(c1,c2),3))
    stop=time()
    print 'the consumed time is:'+str(stop-start)+'seconds' 
#----------------------------------------------------------------------------#
if __name__=='__main__':
    main()