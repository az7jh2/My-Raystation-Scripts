# -*- coding: utf-8 -*-
from connect import *
#---------------------------------------------------------------------------------#
def copybeam(patient,beam_set,exam):
    #复制所选射束集参数
    modality = beam_set.Modality  #如Photons
    '''tech = beam_set.PlanGenerationTechnique  #如IMRT'''
    tech = beam_set.DeliveryTechnique   #如SMLC
    pos = beam_set.PatientPosition   #如HeadFirstSupine
    linac = beam_set.MachineReference.MachineName  #MachineReference中没有能量
    fracs = beam_set.FractionationPattern.NumberOfFractions

    #新建计划
    patient.AddNewPlan(PlanName='Copiedplan',ExaminationName=exam)
    plan=patient.TreatmentPlans['Copiedplan']
    #在新计划中新建空白射束集
    plan.AddNewBeamSet(Name='Copied',ExaminationName=exam, MachineName = linac, Modality=modality, TreatmentTechnique = tech, PatientPosition = pos, NumberOfFractions=fracs)

    infos = plan.QueryBeamSetInfo(Filter={'Name':'Copied'})
    new = plan.LoadBeamSet(BeamSetInfo=infos[0])
    
    #复制射束,无法用len来获取原计划射野个数
    
    i=0
    while 1:
        try:
            beam = beam_set.Beams[i]
        #射野中心和能量
            xpos = beam.PatientToBeamMapping.IsocenterPoint.x
            ypos = beam.PatientToBeamMapping.IsocenterPoint.y
            zpos = beam.PatientToBeamMapping.IsocenterPoint.z
            energy = beam.MachineReference.Energy
            name = beam.Name + "_S" + str(i)
            new.CreatePhotonBeam(Energy=energy, Isocenter = {'x':xpos, 'y':ypos, 'z':zpos}, Name = name, GantryAngle = beam.GantryAngle, CouchAngle = beam.CouchAngle, CollimatorAngle = beam.InitialCollimatorAngle)
            new.Beams[i].BeamMU=beam.BeamMU
            
            j=0
            #读取子野
            while 1:
                try:
                    seg=beam.Segments[j]
                    new.Beams[i].CreateRectangularField()
                    new.Beams[i].Segments[j].JawPositions =  seg.JawPositions 
                    new.Beams[i].Segments[j].LeafPositions = seg.LeafPositions
                    new.Beams[i].Segments[j].RelativeWeight = seg.RelativeWeight
            
                    j=j+1
                except ValueError:
                    break
            
            i+=1
        except ValueError:
            break
#--------------------------------------------------------------------------------------------------------------------------------------------------------------#
#主程序
def main(exam):
    #patient获取为当前患者
    patient=get_current('Patient')
    '''#获取当前计划
    plan=get_current("Plan")'''
    #获取当前射野集
    beam_set=get_current("BeamSet")
    '''#获取CT
    exam=get_current("Examination")'''
    
    #复制射野至指定CT
    copybeam(patient,beam_set,exam)

#-----------------------------------------------------------------------------#
if __name__=='__main__':
    main('CT 1')