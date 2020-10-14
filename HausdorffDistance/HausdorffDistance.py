# -*- coding: utf-8 -*-
#求取指定两个轮廓线的Hausdorff distance
#从Raystation中运行,否则无法连接至Raystation
#----------------------------------------------------------------#
from time import time
start=time()

import sys
sys.path.append('D:\\hill103\\Script\\Hausdorff distance')

#from Distance import *
from DistanceMulti import *

from ROICoordinate import *

from connect import *



#patient获取为当前患者
patient=get_current('Patient')

#examination获取为当前CT序列，CT序列名称在属性Name中，一次只能获取一个CT序列
examination=get_current('Examination')

#StructureSets与CT序列对应，可用object[0],[1],[2]或object['序列名']访问具体的一组Structure
structure_set=patient.PatientModel.StructureSets[examination.Name]

#内置求距离的两个ROI名称，在Raystation运行中无法用raw_input获取键盘输入
#ROI的类型必须为Contour或者mesh，否则报错
x='circle'
y='circle2'
#获取点坐标
c1=RoiCoord(structure_set,x)
c2=RoiCoord(structure_set,y)
#求Hausdorff Distance并输出
print 'the name of current patient is:'+patient.PatientName
print 'the name of current examination is:'+examination.Name
print 'the Hausdorff Distance between '+x+' and '+y+' is:'+str(round(HausDis(c1,c2),3))
stop=time()
print 'the consumed time is:'+str(stop-start)+'seconds' 