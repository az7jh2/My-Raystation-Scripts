# -*- coding: utf-8 -*-
#获取VMAT计划每一个弧的所有控制点的所有叶片位置
#leaf bank坐标为负，right bank坐标为正
from connect import *
import clr
clr.AddReference('Microsoft.Office.Interop.Excel')
from Microsoft.Office.Interop import Excel
#获取一个射野所有子野的CP
def segCP(beam):
    j=0
    LP=[]
    while 1:
        try:
            x=[]
            for m in range(len(beam.Segments[j].LeafPositions)):
                x.append(list(beam.Segments[j].LeafPositions[m]))
            LP.append(x)
            j+=1
        except ValueError:
            break
    return LP
#---------------------------------------------------------------------------#
#获取射野序号、名称、子野
def BeamCP(beam_set):
    beam=[]
    name=[]
    i=0
    while 1:
        try:
            beam.append(segCP(beam_set.Beams[i]))
            name.append(beam_set.Beams[i].Name)
            i+=1
        except ValueError:
            break
    return beam,name
#---------------------------------------------------------------------#
#输出至Excel
def exporttoexcel(a,b):
    #Getting Excel Started
    excel=Excel.ApplicationClass()
    excel.Visible=True
    excel.DisplayAlerts=False
    
    # creating a new one
    workbook=excel.Workbooks.Add()
    
    beamnum=len(a)
    #segnum=len(a[0])    segnum每个射野不一样
    #xnum=len(a[0][0])  xnum总为2
    mlcnum=len(a[0][0][0])
    
    for p1 in range(beamnum):
        # adding a worksheet,每一个sheet代表一个射野
        worksheet=workbook.Worksheets.Add()
        worksheet.Name=b[p1]
        for p2 in range(len(a[p1])):
            #每一个sheet下的所有子野数目，分两列表示
            for p4 in range(mlcnum):
                #excel计数从1开始
                worksheet.Cells(p4+1,p2*2+1).Value=round(a[p1][p2][0][p4],2)
                worksheet.Cells(p4+1,p2*2+1+1).Value=round(a[p1][p2][1][p4],2)
#---------------------------------------------------------------------------------#
#主程序
def main():
    #patient获取为当前患者
    #patient=get_current('Patient')
    #获取当前计划
    #plan=get_current("Plan")
    #获取当前射野集
    beam_set=get_current("BeamSet")
    
    #求控制点
    [x,y]=BeamCP(beam_set)
    #输出至excel
    exporttoexcel(x,y)
#-----------------------------------------------------------------------------#
if __name__=='__main__':
    main()