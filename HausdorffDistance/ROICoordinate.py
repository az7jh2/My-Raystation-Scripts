# -*- coding: utf-8 -*-
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
        contour=roi_geometries.PrimaryShape.Contours
        #记录所有点的坐标，结果为一列表
        for i in range(len(contour)):
            for j in range(len(contour[i])):
                c1.append([contour[i][j].x,contour[i][j].y,contour[i][j].z])
    elif hasattr(roi_geometries.PrimaryShape,'Vertices'):
        contour=roi_geometries.PrimaryShape.Vertices
        #指定ROI的长度len为其所含的点数，类型为list，可用Vertices[0],[1]访问
        #每一个点长度len为3，用Vertices[0].x,y,z来分别获取坐标
        for i in range(len(contour)):
            c1.append([contour[i].x,contour[i].y,contour[i].z])
    else:
        print 'type of ROI is not matched'
    return c1