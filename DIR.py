# -*- coding: utf-8 -*-
from connect import *
#求均匀性指数HI
def GetHomogenietyIndex(total_dose, Prescription, RoiName):
    #total_dose存在于Patient.TreatmentDelivery.TreatmentCourse.TotalDose
    #Prescription可输入数字，或者在getcurrentBeamSet.Prescription.PrimaryDosePrescription.DoseValue,此处还有OnStructure.Name
    #RoiName可用字符串自定义，或者在Patient.PatientModel.StructureSets[Examinations.Name].RoiGeometries[number].OfRoi.Name
    Doses = total_dose.GetDoseAtRelativeVolumes(RoiName = RoiName, RelativeVolumes = [0.02, 0.98])
    #GetDoseAtRelativeVolumes是搜索DVH上点的RayStation自带方法,调用时必须有等号前面部分，第一个参数是字符串，第二个参数是列表
    #返回Doses为Array[float]类型
    Value = (Doses[0]-Doses[1])/Prescription
    return Value
#-----------------------------------------------------------------------------------------------------------#
#求适形度指数CI
def GetConformationIndex(total_dose, DoseValue, RoiName, externalname):
    TotalDoseVolume = total_dose.GetRelativeVolumeAtDoseValues(RoiName = externalname, DoseValues = [DoseValue])
    #GetRelativeVolumeAtDoseValues是搜索DVH上点的RayStation自带方法，返回Array[float]类型
    DoseGridRoi = total_dose.GetDoseGridRoi(RoiName = RoiName)
    #GetDoseGridRoi返回ROI的剂量网格表示
    #返回类型为ScriptObject，下属InDoseGrid,OfRoiGeometry,RoiVolumeDistribution,VersioningStatus四个方法
    #RoiVolumeDistribution下属AlgorithmVersion，RelativeVolumes,TotalVolume，VoxelIndices四个方法
    ExternalRoi = total_dose.GetDoseGridRoi(RoiName = externalname)
    TotalTargetVolume = DoseGridRoi.RoiVolumeDistribution.TotalVolume #target总体积，float类型
    AbsoluteDoseVolume = TotalDoseVolume[0]* ExternalRoi.RoiVolumeDistribution.TotalVolume #用第一个元素做运算，否则视为矩阵运算
    return AbsoluteDoseVolume/TotalTargetVolume
#----------------------------------------------------------------------------------------------------#
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
#------------------------------------------------------------------------------------------------------#
#求一致性指数CN     
def GetConformationNumber(total_dose, DoseValue, RoiName, externalname):
    TargetDoseVolume = total_dose.GetRelativeVolumeAtDoseValues(RoiName = RoiName, DoseValues = [DoseValue])
    TotalDoseVolume = total_dose.GetRelativeVolumeAtDoseValues(RoiName = externalname, DoseValues = [DoseValue])
    DoseGridRoi= total_dose.GetDoseGridRoi(RoiName = RoiName)
    ExternalRoi = total_dose.GetDoseGridRoi(RoiName = externalname)
    TotalTargetVolume = DoseGridRoi.RoiVolumeDistribution.TotalVolume
    AbsoluteTargetDoseVolume = TargetDoseVolume[0]*TotalTargetVolume
    AbsoluteDoseVolume = TotalDoseVolume[0]* ExternalRoi.RoiVolumeDistribution.TotalVolume
    return (AbsoluteTargetDoseVolume* AbsoluteTargetDoseVolume)/(AbsoluteDoseVolume*TotalTargetVolume)
#--------------------------------------------------------------------------------------------------------------#
#求适形指数COnformal INdex
def GetCOnformalINdex(total_dose,DoseValue,TargetName,OrgansName, externalname):
    temp=[1-GetAbsoluteDoseVolume(total_dose, DoseValue,i)/GetAbsoluteVolume(total_dose,i) for i in OrgansName]
    return GetConformationNumber(total_dose, DoseValue, TargetName, externalname)*reduce(lambda a,b:a*b,temp)
#------------------------------------------------------------------------------------------------------------#
def main(dosename, targets, organs, prescription):
    #patient获取为当前患者
    patient = get_current('Patient')
    planlist = []
    doselist = []
    #寻找外轮廓
    try:
        external_roi = next(r for r in patient.PatientModel.RegionsOfInterest if r.Type == 'External')
    except:
        raise Exception('No external ROI defined')
    externalname = external_roi.Name
    for plan in patient.TreatmentPlans:
        planlist.append(plan.Name)
	#添加评估剂量，评估剂量不能用名称访问
    for ev in patient.TreatmentDelivery.FractionEvaluations[0].DoseOnExaminations[0].DoseEvaluations:
        doselist.append(ev.Name)
    #获取剂量
    if dosename in planlist:
        total_dose = patient.TreatmentPlans[dosename].TreatmentCourse.TotalDose
    elif dosename in doselist:
        total_dose = patient.TreatmentDelivery.FractionEvaluations[0].DoseOnExaminations[0].DoseEvaluations[doselist.index(dosename)]
    for i in range(len(targets)):
        print 'the Absolute Volume of '+targets[i]+' is:'+str(round(GetAbsoluteVolume(total_dose,targets[i]),3))
        print 'the Homogeniety Index of '+targets[i]+' is:'+str(round(GetHomogenietyIndex(total_dose, prescription, targets[i]),3))
        print 'the Conformation Index of '+targets[i]+' is:'+str(round(GetConformationIndex(total_dose, prescription, targets[i], externalname),3))
        print 'the Conformation Number of '+targets[i]+' is:'+str(round(GetConformationNumber(total_dose, prescription, targets[i], externalname),3))
        print 'the COnformal INdex of '+targets[i]+' is:'+str(round(GetCOnformalINdex(total_dose,prescription,targets[i],organs, externalname),3))
#--------------------------------------------------------------------------------------------------------------#
if __name__=='__main__':
    main(dosename = 'P1-33', targets = ['PGTV'], organs = ['Parotid gland L','Parotid gland R', 'Brain-sterm'], prescription = 7200)