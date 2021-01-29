# -*- coding: utf-8 -*-
#剂量统计
#python中，空为false
#created by Ningshan Li 2015/7/2
from connect import *
from collections import OrderedDict
import clr
clr.AddReference('Microsoft.Office.Interop.Excel')
from Microsoft.Office.Interop import Excel
#-------------------------------------------------------------------------------------------------------------#
#求ROI的某剂量覆盖绝对体积
#在DVH中找出该剂量对应的相对体积，乘以该ROI的绝对全部体积
def GetAbsoluteDoseVolume(total_dose, DoseValue,RoiName):
    RelativeVolume=total_dose.GetRelativeVolumeAtDoseValues(RoiName = RoiName, DoseValues = [DoseValue])
    DoseGridRoi = total_dose.GetDoseGridRoi(RoiName = RoiName)
    TotalRoiVolume = DoseGridRoi.RoiVolumeDistribution.TotalVolume
    return (TotalRoiVolume*RelativeVolume[0])
#-------------------------------------------------------------------------------------------------------------#           
#求ROI的绝对体积
def GetAbsoluteVolume(total_dose,RoiName):
    DoseGridRoi = total_dose.GetDoseGridRoi(RoiName = RoiName)
    TotalRoiVolume = DoseGridRoi.RoiVolumeDistribution.TotalVolume
    return TotalRoiVolume
#--------------------------------------------------------------------------------------------------------------#
#求适形度指数CI
def GetConformationIndex(total_dose, DoseValue, RoiName,extername):
    TotalTargetVolume = GetAbsoluteVolume(total_dose, RoiName) #target总体积，float类型
    TotalDoseVolume = GetAbsoluteDoseVolume(total_dose,DoseValue,extername)
    TargetDoseVolume = GetAbsoluteDoseVolume(total_dose,DoseValue,RoiName)
    return TargetDoseVolume*TargetDoseVolume/(TotalDoseVolume*TotalTargetVolume)
#------------------------------------------------------------------------------------------------------------#
#输出至Excel
def exporttoexcel(patientname,total_outcome,plans):
    #Getting Excel Started
    excel=Excel.ApplicationClass()
    excel.Visible=True
    excel.DisplayAlerts=False
    
    # creating a new one
    workbook=excel.Workbooks.Add()
    worksheet=workbook.Worksheets.Add()
    
    worksheet.Cells(2,1).Value=patientname
    #excel坐标从1开始算，而range从0开始
    #写入表头信息
    i=0
    for p1 in range(len(plans)):
            #多个字典
        for d in total_outcome[p1]:
            #字典遍历          
            for k,v in d.items():
                if not(k=='roiname'):
                    worksheet.Cells(1,2+i).Value=plans[p1]+'_'+d['roiname']+'_'+k
                    worksheet.Cells(2,2+i).Value=v
                    i+=1
#---------------------------------------------------------------------------------#
def check(gather,objects):
    index=range(len(objects))
    index.reverse()
    for i in index:
        if isinstance(objects[i],str): #列表中的对象为str类型，表明是planlist的名称判断
            if not(objects[i] in gather):
                objects.remove(objects[i])
        elif isinstance(objects[i],dict): #列表中的对象为dict类型，表明是oarlist的名称判断
            if not(objects[i]['name'] in gather):
                objects.remove(objects[i])
#-------------------------------------------------------------------------------------#
def getdoseindicators(total_dose,ROI,extername):
    d=OrderedDict()
    d['roiname']=ROI['name']
    if ROI['Ds']: # Dose指标不为空
        Doses = total_dose.GetDoseAtRelativeVolumes(RoiName = ROI['name'], RelativeVolumes = [i/100.0 for i in ROI['Ds']])
        for i in range(len(ROI['Ds'])):
            name='D'+str(ROI['Ds'][i])
            d[name]=Doses[i]
    if ROI['Vs']: # Volume指标不为空
        Volumes = total_dose.GetRelativeVolumeAtDoseValues(RoiName = ROI['name'], DoseValues=[i*100.0 for i in ROI['Vs']])
        for i in range(len(ROI['Vs'])):
            name='V'+str(ROI['Vs'][i])
            d[name]=Volumes[i]
    if ROI['special']: #特殊类型不为空
        for j in ROI['special']:
            if cmp(j,'max')==0: #查询max
                d['DMax'] = total_dose.GetDoseStatistic(RoiName = ROI['name'], DoseType='Max')
            elif cmp(j,'mean')==0:
                d['DAve'] = total_dose.GetDoseStatistic(RoiName = ROI['name'], DoseType='Average')
            elif cmp(j,'HI')==0:
                try:
                    d['HI']=(d['D2']-d['D98'])/d['D50']  #如果字典中包含这些数值，就直接用
                except: #如果没有，就重新计算
                    tmpdose = total_dose.GetDoseAtRelativeVolumes(RoiName = ROI['name'], RelativeVolumes = [0.02,0.5,0.98])
                    d['HI']=(tmpdose[0]-tmpdose[2])/tmpdose[1]
            elif cmp(j,'CI')==0:
                d['CI']=GetConformationIndex(total_dose, ROI['prescription'], ROI['name'],extername)
            elif j.find('cc')!=-1: #绝对体积相关的剂量学指标,-1表示找不到
                cc=j[0:j.find('cc')]  #绝对体积数
                totalv=GetAbsoluteVolume(total_dose,ROI['name']);
                tmpdose = total_dose.GetDoseAtRelativeVolumes(RoiName = ROI['name'], RelativeVolumes = [float(cc)/totalv])
                d[j]=tmpdose[0]
            elif cmp(j,'Volume')==0:
                d[j]=GetAbsoluteVolume(total_dose,ROI['name'])
    return d
#---------------------------------------------------------------------------------#
def main(patients,plans,targets,OARs):
    if not patients:  #patients不为空
        patient=get_current('Patient')
    #检查对象是否存在
        planlist=[]
        for plan in patient.TreatmentPlans:
            planlist.append(plan.Name)
    
        examination=get_current('Examination')
        structure_set=patient.PatientModel.StructureSets[examination.Name]
        roilist=[]
        for rg in structure_set.RoiGeometries:
            roilist.append(rg.OfRoi.Name)
    #同时遍历和删除，推荐用倒序    
        check(planlist,plans)
        check(roilist,targets)
        check(roilist,OARs)
        #寻找外轮廓
        try:
            external_roi = next(r for r in patient.PatientModel.RegionsOfInterest if r.Type == 'External')
        except:
            raise Exception('No external ROI defined')
        extername=external_roi.Name
    #统计
        total_outcome=[]
        for plan in plans:
            total_dose=patient.TreatmentPlans[plan].TreatmentCourse.TotalDose
            outcome=[]
            for PTV in targets:
                outcome.append(getdoseindicators(total_dose,PTV,extername))
        
            for OAR in OARs:
                outcome.append(getdoseindicators(total_dose,OAR,extername))
          
        total_outcome.append(outcome)
        exporttoexcel(patient.PatientName,total_outcome,plans)
#--------------------------------------------------------------------------------------------------------------#
if __name__=='__main__':
    main(patients=[],plans=['Copy'],targets=[{'name':'APGTVnx','Ds':[2,50,95,98],'Vs':[],'special':['CI','HI','Volume'],'prescription':7400},
    {'name':'APGTVnd','Ds':[2,50,95,98],'Vs':[],'special':['CI','HI','Volume'],'prescription':7000},
    {'name':'APCTV1','Ds':[2,50,95,98],'Vs':[],'special':['CI','HI','Volume'],'prescription':6000},
    {'name':'APCTV2+APCTVnd','Ds':[2,50,95,98],'Vs':[],'special':['CI','HI','Volume'],'prescription':5400}],
    OARs=[{'name':'Brain Stem+3 PRV','Ds':[50],'Vs':[10,15,20,25,30,35,40,45,50,54,55,60],'special':['max']},
    {'name':'Spinal Cord+5 PRV','Ds':[1,5,10,50],'Vs':[50],'special':['max']},
    {'name':'Temporal Lobe L','Ds':[],'Vs':[60,65,70],'special':['max','mean','0.5cc','1cc']},
    {'name':'Temporal Lobe L PRV','Ds':[],'Vs':[],'special':['max','mean']},
    {'name':'Temporal Lobe R','Ds':[],'Vs':[60,65,70],'special':['max','mean','0.5cc','1cc']},
    {'name':'Temporal Lobe R PRV','Ds':[],'Vs':[],'special':['max','mean']},
    {'name':'Optic Chiasm PRV','Ds':[1,5,10],'Vs':[],'special':['max','mean']},
    {'name':'Optic Nerver L PRV','Ds':[1,5,10],'Vs':[],'special':['max','mean']},
    {'name':'Optic Nerve R PRV','Ds':[1,5,10],'Vs':[],'special':['max','mean']},
    {'name':'Ear L','Ds':[],'Vs':[],'special':['max','mean']},
    {'name':'Ear R','Ds':[],'Vs':[],'special':['max','mean']},
    {'name':'Parotid gland L','Ds':[],'Vs':[30],'special':['mean']},
    {'name':'Parotid gland R','Ds':[],'Vs':[30],'special':['mean']}])