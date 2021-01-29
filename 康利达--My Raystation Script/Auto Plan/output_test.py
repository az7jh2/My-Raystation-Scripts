#Created by Ningshan Li 2015-8-20
#output objective parameters
#If function values are not calculated, the objective 'FunctionValue' will be None
from connect import *
#----------------------------------------------------------------------------#
def main():
    plan=get_current('Plan')
    for optimization in plan.PlanOptimizations:
        objectives=optimization.Objective.ConstituentFunctions
        for objective in objectives:
            if hasattr(objective.DoseFunctionParameters,'FunctionType'):
                if 'Dose' in objective.DoseFunctionParameters.FunctionType:
                    print 'ROI:{0}'.format(objective.ForRegionOfInterest.Name)
                    print 'ROI Type:{0}'.format(objective.ForRegionOfInterest.Type)
                    print 'Object Type:{0}'.format(objective.DoseFunctionParameters.FunctionType)
                    print 'DoseLevel:{0}'.format(objective.DoseFunctionParameters.DoseLevel)
                    print 'Weight:{0}'.format(objective.DoseFunctionParameters.Weight)
                    try:
                        print 'Value:{0}'.format(objective.FunctionValue.FunctionValue)
                    except:
                        print 'Value:None'
                elif 'Dvh' in objective.DoseFunctionParameters.FunctionType:
                    print 'ROI:{0}'.format(objective.ForRegionOfInterest.Name)
                    print 'ROI Type:{0}'.format(objective.ForRegionOfInterest.Type)
                    print 'Object Type:{0}'.format(objective.DoseFunctionParameters.FunctionType)
                    print 'DoseLevel:{0}'.format(objective.DoseFunctionParameters.DoseLevel)
                    print 'Volume:{0}'.format(objective.DoseFunctionParameters.PercentVolume)
                    print 'Weight:{0}'.format(objective.DoseFunctionParameters.Weight)
                    try:
                        print 'Value:{0}'.format(objective.FunctionValue.FunctionValue)
                    except:
                        print 'Value:None'
                elif 'Eud' in objective.DoseFunctionParameters.FunctionType:
                    print 'ROI:{0}'.format(objective.ForRegionOfInterest.Name)
                    print 'ROI Type:{0}'.format(objective.ForRegionOfInterest.Type)
                    print 'Object Type:{0}'.format(objective.DoseFunctionParameters.FunctionType)
                    print 'DoseLevel:{0}'.format(objective.DoseFunctionParameters.DoseLevel)
                    print 'Parameter A:{0}'.format(objective.DoseFunctionParameters.EudParameterA)
                    print 'Weight:{0}'.format(objective.DoseFunctionParameters.Weight)
                    try:
                        print 'Value:{0}'.format(objective.FunctionValue.FunctionValue)
                    except:
                        print 'Value:None'
            elif hasattr(objective.DoseFunctionParameters,'HighDoseLevel'):
                # Dose falloff function does not have function type attribute
                print 'ROI:{0}'.format(objective.ForRegionOfInterest.Name)
                print 'ROI Type:{0}'.format(objective.ForRegionOfInterest.Type)
                print 'Object Type:{0}'.format('DoseFallOff')
                print 'HighDoseLevel:{0}'.format(objective.DoseFunctionParameters.HighDoseLevel)
                print 'LowDoseLevel:{0}'.format(objective.DoseFunctionParameters.LowDoseLevel)
                print 'Distance:{0}cm'.format(objective.DoseFunctionParameters.LowDoseDistance)
                print 'Weight:{0}'.format(objective.DoseFunctionParameters.Weight)
                try:
                    print 'Value:{0}'.format(objective.FunctionValue.FunctionValue)
                except:
                    print 'Value:None'
            else:
                raise ('Unknown function type')
                
            
#-----------------------------------------------------------------------------#
if __name__=='__main__':
    main()