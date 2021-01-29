#Created by Ningshan Li 2015-8-26
#print MUs of each beam 
#refer as the current beamset
from connect import *
#----------------------------------------------------------------------------#
def main():
    beamset=get_current('BeamSet')
    print 'The current selected beamset is {0}'.format(beamset.DicomPlanLabel)
    MUsum=0
    for beam in beamset.Beams:
        print 'The MU of beam {0} is: {1}'.format(beam.Name,beam.BeamMU)
        MUsum+=beam.BeamMU
    print 'The total MU of the selected beamset is: {0}'.format(MUsum)
#-----------------   ----------------------------------------------------------#
if __name__=='__main__':
    main()