# -*- coding: utf-8 -*-
#获取指定点的剂量
#Created by Ningshan Li , 2015/7/7

from connect import *
import clr
clr.AddReference('Microsoft.Office.Interop.Excel')
from Microsoft.Office.Interop import Excel
#------------------------------------------------------------------------------#
def getpdd(total_dose,p):
    points=[]
    for i in p:
        points.append({'x':0,'y':i,'z':0})
    doses=total_dose.InterpolateDoseInPoints(Points=points)
    return doses
#------------------------------------------------------------------------------#
def getprofile(total_dose,p,mode,depth):
    points=[]
    for i in p:
        if mode=='Right-Left':
            points.append({'x':i,'y':depth,'z':0})
        elif mode=='Inf-Sup':
            points.append({'x':0,'y':depth,'z':i})
        else:
            raise RuntimeError('The selected mode is wrong')
    doses=total_dose.InterpolateDoseInPoints(Points=points)
    return doses
#-------------------------------------------------------------------------------#        
#输出至Excel
def exporttoexcel(Doses,Names,title,p):
    #Getting Excel Started
    excel=Excel.ApplicationClass()
    excel.Visible=True
    excel.DisplayAlerts=False
    
    # creating a new one
    workbook=excel.Workbooks.Add()
    for p2 in range(len(Names)):
        # adding a worksheet,每一个sheet代表一个射野
        worksheet=workbook.Worksheets.Add()
        worksheet.Name=Names[p2]
        
    #excel坐标从1开始算，而range从0开始
    #写入表头信息         
        for p1 in range(len(Doses[p2])):
            worksheet.Cells(1,1+p1*3).Value=title[p1]
            worksheet.Cells(1,2+p1*3).Value='Dose(cGy)'
            for p3 in range(len(Doses[p2][p1])):
                worksheet.Cells(p3+2,1+p1*3).Value=p[p3]
                worksheet.Cells(p3+2,2+p1*3).Value=round(Doses[p2][p1][p3],5)
#---------------------------------------------------------------------------------#
def main():
    patient=get_current("Patient")
    planlist=[]
    output=[]
    p=[]
    #读入数组
    f=open('e:/Script/Get Point Dose/Array.txt','r')
    for line in f:
        p.append(float(line))
    f.close()
    for plan in patient.TreatmentPlans:
        planlist.append(plan.Name)
        total_dose=plan.TreatmentCourse.TotalDose
        #PDD
        pdddoses=getpdd(total_dose,p)
        #深度1cm，right to left
        d1RtoLdoses=getprofile(total_dose,p,'Right-Left',-14)
        #深度1cm，Inferior to superior
        d1ItoSdoses=getprofile(total_dose,p,'Inf-Sup',-14)
        #深度5cm，right to left
        d5RtoLdoses=getprofile(total_dose,p,'Right-Left',-10)
        #深度5cm，Inferior to superior
        d5ItoSdoses=getprofile(total_dose,p,'Inf-Sup',-10)
        #深度1cm，right to left
        d15RtoLdoses=getprofile(total_dose,p,'Right-Left',0)
        #深度1cm，Inferior to superior
        d15ItoSdoses=getprofile(total_dose,p,'Inf-Sup',0)
        
        output.append([pdddoses,d1RtoLdoses,d1ItoSdoses,d5RtoLdoses,d5ItoSdoses,d15RtoLdoses,d15ItoSdoses])
    title=['PDD','1cm Right-Left','1cm Inferior-Superior','5cm Right-Left','5cm Inferior-Superior','15cm Right-Left','15cm Inferior-Superior']    
    exporttoexcel(output,planlist,title,p)
#--------------------------------------------------------------------------------------------------------------#
if __name__=='__main__':
    main()