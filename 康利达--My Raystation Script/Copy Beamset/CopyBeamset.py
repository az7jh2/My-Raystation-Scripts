# -*- coding: utf-8 -*-
from connect import *
#---------------------------------------------------------------------------------#
def copybeam(patient,beam_set,exam):
    #复制所选射束集参数
    modality = beam_set.Modality  #如Photons
    '''tech = beam_set.PlanGenerationTechnique  #如IMRT
    tech = beam_set.DeliveryTechnique   #如SMLC'''
    pos = beam_set.PatientPosition   #如HeadFirstSupine
    linac = beam_set.MachineReference.MachineName  #MachineReference中没有能量
    fracs = beam_set.FractionationPattern.NumberOfFractions

    #新建计划
    patient.AddNewPlan(PlanName='Copiedplan',ExaminationName=exam)
    plan=patient.TreatmentPlans['Copiedplan']
    #在新计划中新建空白射束集
    plan.AddNewBeamSet(Name='Copied',ExaminationName=exam, MachineName = linac, Modality=modality, TreatmentTechnique = 'Conformal', PatientPosition = pos, NumberOfFractions=fracs)

    infos = plan.QueryBeamSetInfo(Filter={'Name':'Copied'})
    new = plan.LoadBeamSet(BeamSetInfo=infos[0])
    
    #复制射束,无法用len来获取原计划射野个数
    k=0
    i=0
    while 1:
        try:
            beam = beam_set.Beams[i]
        #射野中心和能量
            xpos = beam.PatientToBeamMapping.IsocenterPoint.x
            ypos = beam.PatientToBeamMapping.IsocenterPoint.y
            zpos = beam.PatientToBeamMapping.IsocenterPoint.z
            energy = beam.MachineReference.Energy
            
            j=0
        #读取子野
            while 1:
                try:
                    name = beam.Name + "_S" + str(j)
                    new.CreatePhotonBeam(Energy=energy, Isocenter = {'x':xpos, 'y':ypos, 'z':zpos}, Name = name, GantryAngle = beam.GantryAngle, CouchAngle = beam.CouchAngle, CollimatorAngle = beam.Segments[j].CollimatorAngle)
            #原射野中的一个子野变成一个独立的新射野
                    new.Beams[k].BeamMU = round(beam.BeamMU * beam.Segments[j].RelativeWeight,2)
                    new.Beams[k].CreateRectangularField()
                    new.Beams[k].Segments[0].JawPositions =  beam.Segments[j].JawPositions 
                    new.Beams[k].Segments[0].LeafPositions = beam.Segments[j].LeafPositions
            
                    k=k+1
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