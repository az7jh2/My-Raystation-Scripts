# -*- coding: utf-8 -*-
#导出DVH到Excel
#Created by Ningshan Li , 2016/1/29

from connect import *
import math
import clr
clr.AddReference('Microsoft.Office.Interop.Excel')
from Microsoft.Office.Interop import Excel
#----------------------------------------------------------------------#
def getarray(maxnum, num):
    interval = float(maxnum - 0) / num
    A = []
    for i in range(num+1):
        A.append(0 + i * interval)
    return A
#------------------------------------------------------------------------#
def getDVH(total_dose, roiname, num):
    outcome = {}
    #求该ROI的剂量最大值，即0%体积的剂量
    maxdose = math.ceil(total_dose.GetDoseAtRelativeVolumes(RoiName = roiname, RelativeVolumes = [0.0])[0])
    #生成所需的采样点
    outcome['doses'] = getarray(maxdose, num)
    #获得对应百分体积
    outcome['volumes'] = total_dose.GetRelativeVolumeAtDoseValues(RoiName = roiname, DoseValues=outcome['doses'])
    outcome['roiname'] = roiname
    return outcome
#----------------------------------------------------------------------------#
#输出至Excel
def exporttoexcel(DVH):
    #Getting Excel Started
    excel = Excel.ApplicationClass()
    excel.Visible = True
    excel.DisplayAlerts = False
    
    # creating a new one
    workbook = excel.Workbooks.Add()
    worksheet = workbook.Worksheets.Add()
    
    #excel坐标从1开始算，而range从0开始
    #写入表头信息
    for p1 in range(len(DVH)):
            #多个字典
        worksheet.Cells(1,1+p1*3).Value = DVH[p1]['roiname'] + 'Dose(cGy)'
        worksheet.Cells(1,2+p1*3).Value = DVH[p1]['roiname'] + 'Volumes(%)'
        #遍历字典
        for p2 in range(len(DVH[p1]['doses'])):
                worksheet.Cells(p2+2,1+p1*3).Value = round(DVH[p1]['doses'][p2], 3)
                worksheet.Cells(p2+2,2+p1*3).Value = round(DVH[p1]['volumes'][p2] * 100.0, 3)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------#
#主程序
def main(dosename, num):
    #patient获取为当前患者
    patient = get_current('Patient')
    doselist = []
    planlist = []
    for plan in patient.TreatmentPlans:
        planlist.append(plan.Name)
    
    examination = get_current('Examination')
    structure_set = patient.PatientModel.StructureSets[examination.Name]
    roilist = []
    for rg in structure_set.RoiGeometries:
        roilist.append(rg.OfRoi.Name)
    #添加评估剂量，评估剂量不能用名称访问
    for ev in patient.TreatmentDelivery.FractionEvaluations[0].DoseOnExaminations[0].DoseEvaluations:
        doselist.append(ev.Name)
    #获取剂量
    if dosename in planlist:
        total_dose = patient.TreatmentPlans[dosename].TreatmentCourse.TotalDose
    elif dosename in doselist:
        total_dose = patient.TreatmentDelivery.FractionEvaluations[0].DoseOnExaminations[0].DoseEvaluations[doselist.index(dosename)]
    #获取DVH
    DVH = []
    for roi in roilist:
        DVH.append(getDVH(total_dose, roi, num))
    #输出至EXCEL
    exporttoexcel(DVH)
    return 1
#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    r = main(dosename = 'P1-33', num = 400)
    if r == 1:
        print 'succeed'
    else:
        print 'failed'