# -*- coding: utf-8 -*-
#Created by Ningshan Li 2015-8-24
#automated edit function parameters
#If function values are not calculated, the objective 'FunctionValue' will be None
#循环次数完毕时会自动停止，一次循环中无任何修改会自动停止
#value值和weight也有关系
from connect import *
#----------------------------------------------------------------------------#
def main(low, high, t, change):
    plan = get_current('Plan')
    #suppose only one optimization in the plan
    beamset = get_current('BeamSet')
    #record prescription
    dosetype = beamset.Prescription.PrimaryDosePrescription.PrescriptionType
    dosevalue = beamset.Prescription.PrimaryDosePrescription.DoseValue
    dosevolume = beamset.Prescription.PrimaryDosePrescription.DoseVolume
    roiname = beamset.Prescription.PrimaryDosePrescription.OnStructure.Name
    objectives = plan.PlanOptimizations[0].Objective.ConstituentFunctions
    i=0
    while i <= t:
        flag = 0
        for objective in objectives:
            if objective.ForRegionOfInterest.Type in ['Gtv', 'Ctv', 'Ptv']:  #靶区不改动
                continue
            elif objective.ForRegionOfInterest.Name.upper().find('LEN') != -1:   #晶体不修改
                continue
            else:
                if hasattr(objective.DoseFunctionParameters, 'FunctionType'):
                    try:
                        value = objective.FunctionValue.FunctionValue
                    except:
                        continue
                    if value < low:
                        objective.DoseFunctionParameters.DoseLevel -= change
                        flag = 1
                    elif value>high:
                        objective.DoseFunctionParameters.DoseLevel += change
                        flag = 1
                else:
                    continue
        if flag == 0:
            break
        beamset.NormalizeToPrescription(RoiName =roiname, DoseValue = dosevalue, DoseVolume = dosevolume,
          PrescriptionType = dosetype, EvaluateAfterScaling = True)
        i += 1  
#-----------------   ----------------------------------------------------------#
if __name__ == '__main__':
    main(low = 0.001, high = 0.002, t = 2, change = 50)