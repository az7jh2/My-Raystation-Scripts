# -*- coding: utf-8 -*-
from connect import *
patient=get_current('Patient')
examination=get_current('Examination')
structure_set=patient.PatientModel.StructureSets[examination.Name]
roi_geometries=structure_set.RoiGeometries['PCTV2']
'''c=[]
flag=0
if hasattr(roi_geometries.PrimaryShape,'Contours'):
    #ROI的类型为Contours
    contour=roi_geometries.PrimaryShape.Contours
    #头脚方向为z方向
    for i in range(len(contour)):
        z=contour[i][0].z
        for j in range(len(contour[i])):
            if contour[i][j].z!=z:
                flag=1
        c.append(z)
print flag
print c
d=c
d.sort()
print d
print min(c)  #-89.56cm
print max(c)  #-80.56cm

#测试结果表明，在contour[i]下的所有点都是同一CT层，也就是具有同样的z坐标
#另外contour[i]的z坐标排列也是无序的
#最大和最小值与RayStation一致'''
#采用GetBoundingBox函数来获取范围
bbox = roi_geometries.GetBoundingBox()  #bbox的类型为List[object]，长度为2
for i in [0 , bbox.Count - 1]:        #bbox只有三个属性:x,y,z
    print bbox[i].x
    print bbox[i].y
    print bbox[i].z
    
#bbox[0].z=-89.71,bbox[1].z=-80.41,z的范围比读取轮廓获取的范围广