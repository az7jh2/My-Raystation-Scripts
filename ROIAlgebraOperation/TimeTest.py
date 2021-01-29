# -*- coding: utf-8 -*-
#测试外扩15cm和外扩3*5cm的时间
from connect import *
from time import time
#-------------------------------------------------------------------------------#
def creatmargins(patient,examination,roi,roiname,name,r1,r2):
    patient.PatientModel.CreateRoi(Name=name,Type='Undefined')
    roi[name].CreateMarginGeometry(Examination=examination,SourceRoiName=roiname,
      MarginSettings={ 'Type': "Expand", 'Superior' : r1, 'Inferior': r1, 
      'Anterior': r2, 'Posterior': r2, 'Right': r2, 'Left': r2 })
#------------------------------------------------------------------------------------#
#主程序
def main(ROI):
    patient=get_current('Patient')
    examination=get_current('Examination')
    roi=patient.PatientModel.RegionsOfInterest
    start=time()
    creatmargins(patient,examination,roi,ROI,'bodys1',2,15)
    stop=time()
    print 'the consumed time is:'+str(stop-start)+'seconds' 
    
    start=time()
    creatmargins(patient,examination,roi,ROI,'temp1',0,5)
    creatmargins(patient,examination,roi,'temp1','temp2',0,5)
    creatmargins(patient,examination,roi,'temp2','bodys2',2,5)
    stop=time()
    print 'the consumed time is:'+str(stop-start)+'seconds' 
    
#-----------------------------------------------------------------------------#
if __name__=='__main__':
    main('PCTV') 