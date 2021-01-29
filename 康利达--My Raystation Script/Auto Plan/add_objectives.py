# -*- coding: utf-8 -*-
#Created by Ningshan Li 2016-1-12
#Automatically add objectives of PTV and Rings according to presciption

from connect import *
#----------------------------------------------------------------------------#
def addobjective(opt, Function, dose, weight, roiname):
    with CompositeAction('Add Optimization Function'):
        retval = opt.AddOptimizationFunction(FunctionType = Function, RoiName = roiname)
        retval.DoseFunctionParameters.DoseLevel = dose
        retval.DoseFunctionParameters.Weight = weight
        if 'Dvh' in Function:
            retval.DoseFunctionParameters.PercentVolume = 95
#----------------------------------------------------------------------------#
def main(**p):
    plan = get_current('Plan')
    beamset = get_current('BeamSet')
    #获取处方
    if len(p)==0:
        dose = beamset.Prescription.PrimaryDosePrescription.DoseValue
        roiname = beamset.Prescription.PrimaryDosePrescription.OnStructure.Name
    else:
        dose = p['dose']
        roiname = p['roiname']
    opt = plan.PlanOptimizations[0]
    #增加条件
    addobjective(opt, 'MinDose', dose-50, 85, roiname)
    addobjective(opt, 'MinDvh', dose, 100, roiname)
    addobjective(opt, 'UniformDose', dose+50, 20, roiname)
    addobjective(opt, 'MaxDose', dose+200, 20, roiname)
    addobjective(opt, 'MaxDose', dose-100, 22, 'Ring 1 '+roiname)
    addobjective(opt, 'MaxDose', dose-400, 25, 'Ring 2 '+roiname)
    addobjective(opt, 'MaxDose', dose-700, 27, 'Ring 3 '+roiname)
    addobjective(opt, 'MaxDose', dose-1000, 30, 'Ring 4 '+roiname)
    addobjective(opt, 'MaxDose', dose-1200, 32, 'Ring 5 '+roiname)
    addobjective(opt, 'MaxDose', dose-1500, 35, 'NT')
#-----------------------------------------------------------------------------#
if __name__=='__main__':
    main(roiname = 'CTV', dose = 7000)