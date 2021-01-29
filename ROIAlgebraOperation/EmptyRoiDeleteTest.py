# -*- coding: utf-8 -*-
#删除没有勾画的空ROI
#空ROI的特征是PrimaryShape为Null类型
#created by Ningshan Li，2015/11/14

from connect import *
from time import time
import ctypes
#-----------------------------------------------------------------
def Mbox(title, text, style):
	ctypes.windll.user32.MessageBoxW(0, text, title, style)
#-----------------------------------------------------------------
start=time()
patient=get_current('Patient')
examination=get_current('Examination')
structure_set=patient.PatientModel.StructureSets[examination.Name]
roigeometries=structure_set.RoiGeometries

deletelist=[]
'''for roi in roigeometries:
    if roi.PrimaryShape==None:   #情形1：PrimaryShape为空
        deletelist.append(roi.OfRoi.Name)
    elif hasattr(roi.PrimaryShape,'Contours'):
        if roi.PrimaryShape.Contours==None:  #情形2：PrimaryShape有Contours对象，但是Contours为空
            deletelist.append(roi.OfRoi.Name)   #或者可以用内置函数HasContours()'''

for roi in roigeometries:
    if not(roi.HasContours()):
        deletelist.append(roi.OfRoi.Name)   #根据时间测试的结果，该函数耗时非常小，结果一致，同时也能识别两种情形的空ROI，并不受Voxels类型的干扰,推荐用该函数
                
for roiname in deletelist:
    patient.PatientModel.RegionsOfInterest[roiname].DeleteRoi()

outputtext=''
if deletelist:
    outputtext='ROI named '+','.join(deletelist)+' are empty and deleted.'
else:
    outputtext='No ROI is empty and nothing will be deleted.'
stop=time()
outputtext=outputtext+'\nThe consumed time is '+str(round(stop-start,2))+'seconds'    
Mbox('Warning' , outputtext , 0)