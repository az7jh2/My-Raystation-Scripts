# -*- coding: utf-8 -*-
connect_ok = True
try:
  from connect import *
except:
  connect_ok = False

import wpf
from System import (DateTime, Windows, Globalization)


import clr
clr.AddReference("System.Core")
import System
clr.ImportExtensions(System.Linq)

from math import sqrt
import threading
#---------------------------------------------------------------------------------------------------#

def EucliDis(a,b):
    return sqrt(sum([pow(a[i]-b[i],2) for i in range(len(a))]))

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
   
def ComputerDistance(structure_set,x,y):
    c1=RoiCoord(structure_set,x)
    c2=RoiCoord(structure_set,y)
    return HausDis(c1,c2)
#-----------------------------------------------------------------------------#    
class MeasurementWindow(Windows.Window):

  # Eventhandler
  def OnDropDownImageSetsClosed(self, sender, event):
    if self.cbImageSets.SelectedItem == 0 or self.cbImageSets.SelectedItem != self.selected_image_set:
      self.lVolA.Content = ""
      self.lVolB.Content = ""
      self.lDice.Content = ""
      #self.lPrec.Content = ""
      #self.lSens.Content = ""
      #self.lSpec.Content = ""

 
  # Eventhandler
  def compute_clicked(self, sender, event):
    self.selected_image_set = self.cbImageSets.SelectedItem
    self.selected_roi_a = self.cbRoiA.SelectedItem
    self.selected_roi_b = self.cbRoiB.SelectedItem

    structureSet=patient.PatientModel.StructureSets[self.selected_image_set]

    rgA = structureSet.RoiGeometries[self.selected_roi_a]
    rgB = structureSet.RoiGeometries[self.selected_roi_b]

    #measures = structureSet.ComparisonOfRoiGeometries(RoiA = self.selected_roi_a, RoiB = self.selected_roi_b)
    
    self.lRoiA.Content = self.selected_roi_a
    self.lRoiB.Content = self.selected_roi_b

    self.lVolA.Content = "{0:.2F}".format(rgA.GetRoiVolume())
    self.lVolB.Content = "{0:.2F}".format(rgB.GetRoiVolume())

    comA = rgA.GetCenterOfRoi()
    comB = rgB.GetCenterOfRoi()

    self.lComA.Content = "({0:.2F},{1:.2F},{2:.2F})".format(comA.x,comA.y, comA.z)
    self.lComB.Content = "({0:.2F},{1:.2F},{2:.2F})".format(comB.x,comB.y, comB.z)

    self.lDice.Content = "{0:.3F}".format(ComputerDistance(structureSet,self.selected_roi_a,self.selected_roi_b))
    #self.lPrec.Content = "{0:.3F}".format(measures["Precision"])
    #self.lSens.Content = "{0:.3F}".format(measures["Sensitivity"])
    #self.lSpec.Content = "{0:.3F}".format(measures["Specificity"])

  def __init__(self, title, imagesets, roigeometries):
    
    wpf.LoadComponent(self, "D:\hill103\Script\Hausdorff Distance\Hausdorff.xaml")

    self.Title = title

    self.cbImageSets.ItemsSource = imagesets
    self.cbRoiA.ItemsSource = roigeometries
    self.cbRoiB.ItemsSource = roigeometries
    self.selected_image_set = 0

    self.bCompute.Click += self.compute_clicked



'''class RoiComparison:
  def __init__(roiA, roiB, volumeA, volumeB, dice, precision):
    self.roiA = roiA
    self.roiB = roiB
    self.volumeA = volumeA
    self.volumeB = volumeB
    self.dice = dice
    self.precision = precision'''

#####################################

if connect_ok:
  patient = get_current("Patient")

  imagesets = []
  for examination in patient.Examinations:
    imagesets.Add(examination.Name)

  roigeometries = []
  for rg in patient.PatientModel.RegionsOfInterest:
    roigeometries.Add(rg.Name)
    
  dialog = MeasurementWindow("Compute Hausdorff Distance",imagesets, roigeometries)
  dialog.ShowDialog()