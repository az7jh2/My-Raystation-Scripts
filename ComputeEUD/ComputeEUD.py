#Created by Ningshan Li 2015-8-26
#compute EUD 
from connect import *
#-------------------------------------------------#
def compute_eud(dose, roiname, a):
    # Get the dose values from the dose distribution
    dose_values = [d for d in dose.DoseValues.DoseData]
    # Get the dose grid representation of the ROI
    dgr = dose.GetDoseGridRoi(RoiName=roiname)
    # Get indices and relative volumes
    indices = dgr.RoiVolumeDistribution.VoxelIndices
    relative_volumes = dgr.RoiVolumeDistribution.RelativeVolumes
    dose_sum = 0
    # Sum the dose values and scale with scalefactor and parameter_a
    for i, v in zip(indices, relative_volumes):
        d = dose_values[i]
        dose_sum += v * (d ** a)
    return dose_sum ** (1 / a)
#------------------------------------------------------#
def main(roinames,a):
    plan = get_current('Plan')
    for roiname in roinames:
        eud = compute_eud(plan.TreatmentCourse.TotalDose, roiname, a)
        print 'EUD with parameter a {0} for ROI {1}: {2} cGy'.format(a, roiname, eud)
#----------------------------------------------------------#
if __name__=='__main__':
    main(roinames=['Parotid L','Parotid R','Mandible L','Mandible R','TMJ L','TMJ R','Spinal Cord'],a=float(1))