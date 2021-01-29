from connect import *
import numpy as np

patient = get_current('Patient')
matr = patient.GetTransformForExaminations(FromExamination='CT 1',ToExamination='CT 2')
tmpstr = ''
for i in range(0 , len(matr)):
	tmpstr += str(matr[i]) + ' '
	if (i + 1) % 4 == 0:
		if i != 15:
			tmpstr += '; '

print('Transformation matrix:')
m = np.matrix(tmpstr)
print (m)
p = np.matrix('0.0 ; 17.11 ; 2.58 ; 1.0')

print ('Manual multiplication result for (0.0 ; 17.11 ; 2.58): ')
print ('x:' + str((m * p).item(0)))
print ('y:' + str((m * p).item(1)))
print ('z:' + str((m * p).item(2)))

a = patient.TransformPointFromExaminationToExaminationUsingTotalTransform(FromExamination='CT 1',ToExamination='CT 2',Point= {'x':0.0, 'y':17.11, 'z':2.58})
print ('x:' + str(a.x))
print ('y:' + str(a.y))
print ('z:' + str(a.z))

a = patient.TransformPointFromExaminationToExamination(FromExamination='CT 1',ToExamination='CT 2',Point= {'x':0.0, 'y':17.11, 'z':2.58})
print ('x:' + str(a.x))
print ('y:' + str(a.y))
print ('z:' + str(a.z))