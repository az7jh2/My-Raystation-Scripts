# -*- coding: utf-8 -*-
from connect import *
patient=get_current('Patient')
examination=get_current('Examination')
structure_set=patient.PatientModel.StructureSets[examination.Name]
roi_geometries=structure_set.RoiGeometries['Bodys']
if hasattr(roi_geometries.PrimaryShape,'Contours'):
    #ROI的类型为Contours
    contour=roi_geometries.PrimaryShape.Contours
    index=range(len(contour))
    index.reverse()
    for i in index:
        if contour[i][0].z>-80.56 or contour[i][0]<-89.56:
            contour.RemoveAt(i)
    
    
    
    

#测试结果表明contour和contour[i]的type为List[object]，contour[i][j]的type为ExpandoObject
#对list使用remove方法，删除的元素位置会被后面的元素填补上
#若要同时遍历和删除，推荐用倒序
#raystation中提供了3种删除元素方法:contour.RemoveAll(),RemoveAt(),RemoveRange(),
#该方法中下标从0开始,不支持负数