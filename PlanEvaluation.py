# -*- coding: utf-8 -*-
#剂量统计
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
def GetConformationIndex(total_dose, DoseValue, RoiName):
    TotalTargetVolume = GetAbsoluteVolume(total_dose, RoiName) #target总体积，float类型
    TotalDoseVolume = GetAbsoluteDoseVolume(total_dose,DoseValue,"External")
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
        if not(objects[i] in gather):
            objects.remove(objects[i])
#---------------------------------------------------------------------------------#
def main(plans,targets,serialOARs,parallelOARs,prescription):
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
    check(roilist,serialOARs)
    check(roilist,parallelOARs)
            
    #统计
    total_outcome=[]
    for plan in plans:
        total_dose=patient.TreatmentPlans[plan].TreatmentCourse.TotalDose
        outcome=[]
        for PTV in targets:
            d=OrderedDict()
            d['roiname']=PTV
            Doses = total_dose.GetDoseAtRelativeVolumes(RoiName = PTV, RelativeVolumes = [0.02,0.5,0.95,0.98])
            d['D2']=Doses[0]
            d['D50']=Doses[1]
            d['D95']=Doses[2]
            d['D98']=Doses[3]
            d['HI']=(Doses[0]-Doses[3])/Doses[1]
            d['CI']=GetConformationIndex(total_dose, prescription, PTV)
            outcome.append(d)
        
        for OAR in serialOARs:
            d=OrderedDict()
            d['roiname']=OAR
            Doses = total_dose.GetDoseAtRelativeVolumes(RoiName = OAR, RelativeVolumes = [0.02,0.5])
            d['D2']=Doses[0]
            d['D50']=Doses[1]
            outcome.append(d)
            
        for OAR in parallelOARs:
            d=OrderedDict()
            d['roiname']=OAR
            if OAR in ['Parotid L','Parotid R','Liver']:
                Doses = total_dose.GetDoseAtRelativeVolumes(RoiName = OAR, RelativeVolumes = [0.5])
                d['D50']=Doses[0]
                Volumes= total_dose.GetRelativeVolumeAtDoseValues(RoiName = OAR,DoseValues=[3000])
                d['V30']=Volumes[0]
            elif OAR=='Thyroid':
                Doses = total_dose.GetDoseAtRelativeVolumes(RoiName = OAR, RelativeVolumes = [0.5])
                d['D50']=Doses[0]
                Volumes= total_dose.GetRelativeVolumeAtDoseValues(RoiName = OAR,DoseValues=[4000,5000])
                d['V40']=Volumes[0]
                d['V50']=Volumes[1]
            elif OAR in ['Lung All','Lung R','Lung L']:
                Doses = total_dose.GetDoseAtRelativeVolumes(RoiName = OAR, RelativeVolumes = [0.5])
                d['D50']=Doses[0]
                d['DAve'] = total_dose.GetDoseStatistic(RoiName = OAR, DoseType='Average')
                Volumes= total_dose.GetRelativeVolumeAtDoseValues(RoiName = OAR,DoseValues=[500,2000])
                d['V5']=Volumes[0]
                d['V20']=Volumes[1]
            elif OAR=='Heart':
                Doses = total_dose.GetDoseAtRelativeVolumes(RoiName = OAR, RelativeVolumes = [0.5])
                d['D50']=Doses[0]
                Volumes= total_dose.GetRelativeVolumeAtDoseValues(RoiName = OAR,DoseValues=[3000,4000])
                d['V30']=Volumes[0]
                d['V40']=Volumes[1]
            elif OAR in ['Humerus Head L','Humerus Head R','Bladder','Rectum','Colon','Femoral head R','Femoral head L','Small Intestine']:
                Doses = total_dose.GetDoseAtRelativeVolumes(RoiName = OAR, RelativeVolumes = [0.02,0.5])
                d['D2']=Doses[0]
                d['D50']=Doses[1]
                Volumes= total_dose.GetRelativeVolumeAtDoseValues(RoiName = OAR,DoseValues=[5000])
                d['V50']=Volumes[0]
            elif OAR in ['Kidney R','Kidney L']:
                Doses = total_dose.GetDoseAtRelativeVolumes(RoiName = OAR, RelativeVolumes = [0.5])
                d['D50']=Doses[0]
                Volumes= total_dose.GetRelativeVolumeAtDoseValues(RoiName = OAR,DoseValues=[2000])
                d['V20']=Volumes[0]
            elif OAR=='Stomach':
                Doses = total_dose.GetDoseAtRelativeVolumes(RoiName = OAR, RelativeVolumes = [0.02,0.5])
                d['D2']=Doses[0]
                d['D50']=Doses[1]
                Volumes= total_dose.GetRelativeVolumeAtDoseValues(RoiName = OAR,DoseValues=[3000])
                d['V30']=Volumes[0]
            else:
                Doses = total_dose.GetDoseAtRelativeVolumes(RoiName = OAR, RelativeVolumes = [0.02,0.5])
                d['D2']=Doses[0]
                d['D50']=Doses[1]
            outcome.append(d)
        total_outcome.append(outcome)
    exporttoexcel(patient.PatientName,total_outcome,plans)
#--------------------------------------------------------------------------------------------------------------#
if __name__=='__main__':
    main(plans=['MCO-test5','Plan_1'],targets=['PTV\''],serialOARs=['Brain Stem','Brain Stem PRV','Spinal Cord','Spinal Cord PRV','Lens L','Lens R'],
      parallelOARs=['Optic Chiasm','Optic Nerver L','Optic Nerve R','Temporal Lobe L','Temporal Lobe R','Parotid L','Parotid R','Larynx','Ear L','Ear R','Piturary',
      'Mandible L','Mandible R','TMJ L','TMJ R','Eye L','Eye R','Lung All','Lung R','Lung L','Heart','Esophagus','Humerus Head L','Humerus Head R','Liver','Stomach',
      'Small Intestine','Kidney R','Kidney L','Bladder','Rectum','Colon','Femoral head R','Femoral head L','Ovaries','Testicles'],prescription=3000)