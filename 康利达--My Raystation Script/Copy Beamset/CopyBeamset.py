# -*- coding: utf-8 -*-
#复制beamset至指定CT
#Created by Ningshan Li 2015-6-23

from connect import *
#---------------------------------------------------------------------------------#
def copybeam(patient,beam_set,exam,isoset):
    #复制所选射束集参数
    modality = beam_set.Modality  #如Photons
    plantech = beam_set.PlanGenerationTechnique  #如IMRT
    '''deliverytech = beam_set.DeliveryTechnique   #如SMLC'''
    pos = beam_set.PatientPosition   #如HeadFirstSupine
    linac = beam_set.MachineReference.MachineName  #MachineReference中没有能量
    fracs = beam_set.FractionationPattern.NumberOfFractions
    if plantech=='Imrt':
        tech='SMLC'
    elif plantech=='Conformal':
        tech='Conformal'
    
    #新建计划
    patient.AddNewPlan(PlanName='Copiedplan',ExaminationName=exam)
    plan=patient.TreatmentPlans['Copiedplan']
    #在新计划中新建空白射束集,治疗技术只能为SMLC或Comformal
    plan.AddNewBeamSet(Name='Copied',ExaminationName=exam, MachineName = linac, Modality=modality, 
      TreatmentTechnique = tech, PatientPosition = pos, NumberOfFractions=fracs)

    infos = plan.QueryBeamSetInfo(Filter={'Name':'Copied'})
    new = plan.LoadBeamSet(BeamSetInfo=infos[0])
    
    #复制射束,无法用len来获取原计划射野个数
    i=0 #记录射野的num，用于赋值
    for beam in beam_set.Beams:
        #射野中心和能量
        if isoset=='Copy from prototype':
            xpos = beam.PatientToBeamMapping.IsocenterPoint.x
            ypos = beam.PatientToBeamMapping.IsocenterPoint.y
            zpos = beam.PatientToBeamMapping.IsocenterPoint.z
        elif isoset=='Zeros':
            xpos=0
            ypos=0
            zpos=0
        else:
            raise RuntimeError('The selected mode of setting isocenter is wrong') 
        energy = beam.MachineReference.Energy
        name = beam.Name + "_Copy"
        
        new.CreatePhotonBeam(Energy=energy, Isocenter = {'x':xpos, 'y':ypos, 'z':zpos}, Name = name, 
          GantryAngle = beam.GantryAngle, CouchAngle = beam.CouchAngle, CollimatorAngle = beam.InitialCollimatorAngle)
        new.Beams[i].BeamMU=beam.BeamMU
            
        #读取子野
        j=0
        for seg in beam.Segments:
            new.Beams[i].CreateRectangularField()
            new.Beams[i].Segments[j].JawPositions =  seg.JawPositions 
            new.Beams[i].Segments[j].LeafPositions = seg.LeafPositions
            new.Beams[i].Segments[j].RelativeWeight = seg.RelativeWeight
            j+=1
            
        i+=1
#--------------------------------------------------------------------------------------------------------------------------------------------------------------#
#主程序
def main(plan,beamset,fromexam,toexam,mode):
    #patient获取为当前患者
    patient=get_current('Patient')
    
   
    beam_set=patient.TreatmentPlans[plan].BeamSets[beamset]
    
    
    #复制射野至指定CT
    copybeam(patient,beam_set,toexam,mode)
    
    #设置网格，计算剂量
    patient.TreatmentPlans['Copiedplan'].SetDefaultDoseGrid(VoxelSize={ 'x': 0.3, 'y': 0.3, 'z': 0.3 })
    patient.TreatmentPlans['Copiedplan'].ComputeRoiVoxelVolumes()
    patient.TreatmentPlans['Copiedplan'].BeamSets['Copied'].ComputeDose(ComputeBeamDoses=True, 
      DoseAlgorithm="CCDose", ForceRecompute=False)

#-----------------------------------------------------------------------------#
if __name__=='__main__':
    main(plan,beamset,fromexam,toexam,mode)