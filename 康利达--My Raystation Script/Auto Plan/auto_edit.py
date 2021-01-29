#Created by Ningshan Li 2015-8-24
#automated edit function parameters
#If function values are not calculated, the objective 'FunctionValue' will be None
from connect import *
#----------------------------------------------------------------------------#
def main(low,high,times,change):
    plan=get_current('Plan')
    #suppose only one optimization in the plan
    objectives=plan.PlanOptimizations[0].Objective.ConstituentFunctions
    for i in range(times):
        for objective in objectives:
            if objective.ForRegionOfInterest.Type in ['Gtv','Ctv','Ptv']:
                continue
            else:
                if hasattr(objective.DoseFunctionParameters,'FunctionType'):
                    try:
                        value=objective.FunctionValue.FunctionValue
                    except:
                        continue
                    if value<low:
                        objective.DoseFunctionParameters.DoseLevel-=change/(2**i)
                    elif value>high:
                        objective.DoseFunctionParameters.DoseLevel+=change/(2**i)
                else:
                    continue
        if i<=0.5*times:
            plan.PlanOptimizations[0].ResetOptimization()
        plan.PlanOptimizations[0].RunOptimization()
#-----------------   ----------------------------------------------------------#
if __name__=='__main__':
    main(low=0.001,high=0.002,times=2,change=300)