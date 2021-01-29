# -*- coding: utf-8 -*-
#复制beamset至指定CT
#Created by Ningshan Li 2015-6-23

from connect import *
import ctypes
#-----------------------------------------------------------------
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxW(0, text, title, style)
#---------------------------------------------------------------------------------#
def copybeam(patient,beamset,fromexamname,toexamname,mode,newplanname,newbeamsetname,POIs):
    #复制所选射束集参数
    modality = beamset.Modality  #如Photons
    plantech = beamset.PlanGenerationTechnique  #如IMRT
    pos = beamset.PatientPosition   #如HeadFirstSupine
    linac = beamset.MachineReference.MachineName  #MachineReference中没有能量
    fracs = beamset.FractionationPattern.NumberOfFractions
    if plantech=='Imrt':
        tech='SMLC'
    elif plantech=='Conformal':
        tech='Conformal'
    
    #新建计划
    patient.AddNewPlan(PlanName=newplanname,ExaminationName=toexamname)
    #载入新建计划
    info=patient.QueryPlanInfo(Filter={'Name':'^{0}$'.format(newplanname)})
    if len(info)==1:
        plan=patient.LoadPlan(PlanInfo=info[0])
    else:
        raise Exception('No plan named {0} exists for the current patient'.format(newplanname))
    #在新计划中新建空白射束集,治疗技术只能为SMLC或Comformal
    plan.AddNewBeamSet(Name=newbeamsetname,ExaminationName=toexamname, MachineName = linac, Modality=modality, 
      TreatmentTechnique = tech, PatientPosition = pos, NumberOfFractions=fracs)

    info = plan.QueryBeamSetInfo(Filter={'Name':'^{0}$'.format(newbeamsetname)})
    if len(info)==1:
        newbeamset = plan.LoadBeamSet(BeamSetInfo=info[0])
    else:
        raise Exception('No beamset named {0} exists for the current plan'.format(newbeamsetname))
    
    #复制射束,无法用len来获取原计划射野个数
    i=0 #记录射野的num，用于赋值
    for beam in beamset.Beams:
        #射野中心和能量
        if mode=='Copy from prototype':
            xpos = beam.PatientToBeamMapping.IsocenterPoint.x
            ypos = beam.PatientToBeamMapping.IsocenterPoint.y
            zpos = beam.PatientToBeamMapping.IsocenterPoint.z
        elif mode=='Zeros':
            xpos=0
            ypos=0
            zpos=0
        elif mode=='Rigid Registration':
            xorgin = beam.PatientToBeamMapping.IsocenterPoint.x
            yorgin = beam.PatientToBeamMapping.IsocenterPoint.y
            zorgin = beam.PatientToBeamMapping.IsocenterPoint.z
            newiso=patient.TransformPointFromExaminationToExaminationUsingTotalTransform(FromExamination=fromexamname,ToExamination=toexamname,
              Point= {'x':xorgin, 'y':yorgin, 'z':zorgin})
            xpos=newiso.x
            ypos=newiso.y
            zpos=newiso.z
        elif mode in POIs:
            newiso=patient.PatientModel.StructureSets[toexamname].PoiGeometries[mode].Point
            xpos=newiso.x
            ypos=newiso.y
            zpos=newiso.z
        else:
            raise RuntimeError('The selected mode of setting isocenter is wrong') 
        energy = beam.MachineReference.Energy
        name = beam.Name + "_Copy"
        
        newbeamset.CreatePhotonBeam(Energy=energy, Isocenter = {'x':xpos, 'y':ypos, 'z':zpos}, Name = name, 
          GantryAngle = beam.GantryAngle, CouchAngle = beam.CouchAngle, CollimatorAngle = beam.InitialCollimatorAngle)
        newbeamset.Beams[i].BeamMU=beam.BeamMU
            
        #读取子野
        j=0
        for seg in beam.Segments:
            newbeamset.Beams[i].CreateRectangularField()
            newbeamset.Beams[i].Segments[j].JawPositions =  seg.JawPositions 
            newbeamset.Beams[i].Segments[j].LeafPositions = seg.LeafPositions
            newbeamset.Beams[i].Segments[j].RelativeWeight = seg.RelativeWeight
            j+=1
            
        i+=1
#--------------------------------------------------------------------------------------------------------------------------------------------------------------#
#主程序
def main(planname,beamsetname,fromexamname,toexamname,mode,newplanname,newbeamsetname):
    #patient获取为当前患者
    patient=get_current('Patient')
    #所有POI
    POIs=[]
    for poi in patient.PatientModel.PointsOfInterest:
        POIs.append(poi.Name)
    #判断计划和射束集
    try:
        beam_set=patient.TreatmentPlans[planname].BeamSets[beamsetname]
    except:
        Mbox('Warning','The selected beamset dose not belong to the selected plan',0)
        return 0
    #判断beamset,CRT或者SMLC的技术都是SMLC
    if not(beam_set.DeliveryTechnique=='SMLC'):
        Mbox('Warning','The selected beamset is not with the technique of SMLC or CRT',0)
        return 0
    #判断plan和fromCT是否一致
    if not(patient.TreatmentPlans[planname].GetStructureSet().OnExamination.Name==fromexamname):
        Mbox('Warning','The selected plan dose not correspond to the select from examination',0)
        return 0
    #判断配准模式下是否存在配准
    if mode=='Rigid Registration':
        if fromexamname==toexamname:
            Mbox('Warning','The selected from examination is identical to the selected to examination',0)
            return 0
        else:
            if patient.GetTotalTransformForExaminations(FromExamination=fromexamname,ToExamination=toexamname)==None:
                Mbox('Warning','There is no rigid registration between selected examinations',0)
                return 0
    #判断新计划名是否存在
    existplannames=[]
    for plan in patient.TreatmentPlans:
        existplannames.append(plan.Name)
    if newplanname in existplannames:
        Mbox('Warning','The inputed name of new plan is already exist',0)
        return 0
    #计算新射束名称位数
    if len(newbeamsetname)>16:
        newbeamsetname=newbeamsetname[:16]
    #判断所选POI是否和CT对应
    if mode in POIs:
        if patient.PatientModel.StructureSets[toexamname].PoiGeometries[mode].Point.x<-10000:
            Mbox('Warning','The selected ISO is not corresponding to the to new CT',0)
            return 0
    #复制射野至指定CT
    copybeam(patient=patient,beamset=beam_set,fromexamname=fromexamname,toexamname=toexamname,mode=mode,newplanname=newplanname,newbeamsetname=newbeamsetname,
      POIs=POIs)
    
    #设置网格，计算剂量
    patient.TreatmentPlans[newplanname].SetDefaultDoseGrid(VoxelSize={ 'x': 0.3, 'y': 0.3, 'z': 0.3 })
    patient.TreatmentPlans[newplanname].ComputeRoiVoxelVolumes()
    patient.TreatmentPlans[newplanname].BeamSets[newbeamsetname].ComputeDose(ComputeBeamDoses=True, 
      DoseAlgorithm="CCDose", ForceRecompute=False)
    return 1
#-----------------------------------------------------------------------------#
if __name__=='__main__':
    r=main(planname='Plan_CT1',beamsetname='Plan_CT1',fromexamname='CT 1',toexamname='CT 1',mode='Zeros',newplanname='test2',newbeamsetname='1')
    print r