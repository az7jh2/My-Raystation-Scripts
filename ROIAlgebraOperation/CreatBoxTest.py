# -*- coding: utf-8 -*-
from connect import *
from time import time
start=time()
patient=get_current('Patient')
examination=get_current('Examination')
structure_set=patient.PatientModel.StructureSets[examination.Name]
roi=patient.PatientModel.RegionsOfInterest
external=structure_set.RoiGeometries['External']
bbox = external.GetBoundingBox()
zmin=-89.71
zmax=-80.41
if bbox.Count!=2:
    raise Exception('The length of bbox is not 2') 
xsize = bbox[1].x - bbox[0].x + 2.0
ysize = bbox[1].y - bbox[0].y + 2.0
zsize = abs(zmax - zmin) + 2.0
xcenter=external.GetCenterOfRoi().x
ycenter=external.GetCenterOfRoi().y
zcenter=zmin+(zmax-zmin)/2

patient.PatientModel.CreateRoi(Name = 'cu' , Color = 'red' , Type = 'Undefined')
size = {"x":xsize , "y": ysize, "z":zsize}
center = {"x":xcenter, "y":ycenter, "z":zcenter}
roi['cu'].CreateBoxGeometry(Size =  size , Examination = examination , Center = center)

patient.PatientModel.CreateRoi(Name = 'bo' , Color = 'green' , Type = 'Undefined')
roi['bo'].SetAlgebraExpression(ExpressionA={ 'Operation': "Union", 'SourceRoiNames': ['External'], 
  'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, 
  ExpressionB={ 'Operation': "Union", 'SourceRoiNames': ['cu'], 
  'MarginSettings': { 'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 'Right': 0, 'Left': 0 } }, 
  ResultOperation="Intersection")
roi['bo'].UpdateDerivedGeometry(Examination=examination)
stop=time()
print 'the consumed time is: {0}seconds'.format(stop-start)
# the consumed time is: 3.7832seconds