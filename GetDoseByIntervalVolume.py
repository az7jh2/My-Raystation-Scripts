# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------------------------------------#           
from connect import *
#from math import floor
import clr
clr.AddReference('Microsoft.Office.Interop.Excel')
from Microsoft.Office.Interop import Excel
#求ROI的绝对体积
def GetAbsoluteVolume(total_dose,RoiName):
    DoseGridRoi = total_dose.GetDoseGridRoi(RoiName = RoiName)
    TotalRoiVolume = DoseGridRoi.RoiVolumeDistribution.TotalVolume
    return TotalRoiVolume
#------------------------------------------------------------------------------------------------------#
#求剂量，以0.1cc为间隔
def GetDose(total_dose,RoiName):
    TotalRoiVolume=GetAbsoluteVolume(total_dose,RoiName)
    #Doses=[[round(float(i)/10,1),round(total_dose.GetDoseAtRelativeVolumes(RoiName = RoiName, RelativeVolumes = [i/(10*TotalRoiVolume)])[0])] for i in range(int(floor(TotalRoiVolume*10)))]
    #Doses.append([round(TotalRoiVolume,1),round(total_dose.GetDoseAtRelativeVolumes(RoiName = RoiName, RelativeVolumes = [1])[0])])
    #range只能用于整数,floor不大于该数的最大整数,返回结果为float
    #整数除以整数结果为整数（1/10=0)
    #GetDoseAtRelativeVolumes每运行一次会出现一次提示，故将要用到的相对体积做成列表后再调用函数
    AbVolume=[] #保存绝对体积
    ReVolume=[] #保存相对体积
    Doses=[]  #保存剂量
    '''for i in range(int(floor(TotalRoiVolume*10))):
        AbVolume.append(round(float(i)/10,1))
        ReVolume.append(i/(10*TotalRoiVolume))  #Ironpython类型转换和四舍五入容易出问题，采用while循环为好'''
    i=0
    while i<TotalRoiVolume:
        AbVolume.append(str(round(i,1))+'cc') #解决数字位数问题，保留一位小数后，再转换成字符串
        ReVolume.append(i/TotalRoiVolume)
        i+=0.1
    #追加100%体积的剂量
    AbVolume.append(str(round(TotalRoiVolume,2))+'cc')
    ReVolume.append(1)
    tempdose=total_dose.GetDoseAtRelativeVolumes(RoiName = RoiName, RelativeVolumes = ReVolume)
    for i in range(len(AbVolume)):
        Doses.append([AbVolume[i],round(tempdose[i],1)]) 
    return Doses
#------------------------------------------------------------------------------------------------------------#
#输出至Excel
def exporttoexcel(Doses):
    #Getting Excel Started
    excel=Excel.ApplicationClass()
    excel.Visible=True
    excel.DisplayAlerts=False
    
    # creating a new one
    workbook=excel.Workbooks.Add()
    
    # adding a worksheet,每一个sheet代表一个射野
    worksheet=workbook.Worksheets.Add()
    worksheet.Name='Dose' 
    
    #excel坐标从1开始算，而range从0开始
    #写入表头信息
    worksheet.Cells(1,1).Value='Volume(cc)'
    worksheet.Cells(1,2).Value='Dose(cGy)'
    
    for p1 in range(len(Doses)):
        worksheet.Cells(p1+2,1).Value=Doses[p1][0]
        worksheet.Cells(p1+2,2).Value=Doses[p1][1]
#---------------------------------------------------------------------------------#
#输出至txt文档
def exporttotxt(Doses):
    #路径为c盘，如果没有文件将会新建，已有文件将完全覆盖
    f=open('c:/Dose.txt','w')
    #write只能写str类型变量，t为制表符，n为回车
    f.write('Volume(cc)'+'\t'+'Dose(cGy)'+'\n')
    
    for p1 in range(len(Doses)):
        f.write(Doses[p1][0]+'\t'+str(Doses[p1][1])+'\n')
    f.close()
#----------------------------------------------------------------------------------#
def main(RoiName,Mode):
    plan=get_current("Plan")
    total_dose=plan.TreatmentCourse.TotalDose
    Doses=GetDose(total_dose,RoiName)
    if Mode=='excel':
        exporttoexcel(Doses)
    elif Mode=='txt':
        exporttotxt(Doses)
    else:
        raise RuntimeError('The selected mode is wrong')  #抛出异常
        
#--------------------------------------------------------------------------------------------------------------#
if __name__=='__main__':
    main('PTV-6996','txt')