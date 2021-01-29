import sys
import dicom 
# print dicom  # check path of dicom module 
import os
dicompath='C:\\DICOM'
dcmfiles=[]
beaminfo=[]
for dirName, subdirList, fileList in os.walk(dicompath):
    for filename in fileList:
        if ".dcm" in filename.lower():  # check whether the file is DICOM
            dcmfiles.append(os.path.join(dirName,filename))
print dcmfiles
print dirName
print subdirList
print fileList
print beaminfo
'''
            for file in dcmfiles:
    ds=dicom.read_file(file)
    if ds.Modality=='RTPLAN':
	    uid=ds.StudyInstanceUID
	    planname=ds.RTPlanName
	    for beams in ds.BeamSequence:
		    beaminfo.append({'beamnum':beams.BeamNumber,'beamname':beams.BeamName})
#rename dose file        
for file in dcmfiles:
    ds=dicom.read_file(file)
    if ds.StudyInstanceUID==uid:
        if ds.Modality=='RTDOSE':
            if ds.DoseSummationType=='PLAN':
                ds.save_as(os.path.join(dirName,planname+'_dose.dcm'))
            elif ds.DoseSummationType=='BEAM':
                for dict in beaminfo:
                    if dict['beamnum']==ds.SeriesNumber:
                        beamname=dict['beamname']
                        break
                ds.save_as(os.path.join(dirName,planname+'_'+beamname+'_dose.dcm'))'''
