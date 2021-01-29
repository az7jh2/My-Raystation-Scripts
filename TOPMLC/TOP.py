# -*- coding: utf-8 -*-
#RayStation到TOP外挂MLC的接口
#Created by Ningshan Li 2015-12-24
#--------------------------------------------------------#
from connect import *
import time
from string import zfill

patient = get_current('Patient')
plan = get_current('Plan')
beamset = get_current('BeamSet')

filename = patient.PatientID + '_' + patient.PatientName + '_' +plan.Name
f = open('e:/' + filename +'.top','w')

if beamset.PlanGenerationTechnique == 'Imrt':
    f.write('Usage = TP_IMRTSTATIC' +'\n')
elif beamset.PlanGenerationTechnique == 'Conformal':
    f.write('Usage = TP_APERTURE' +'\n')
    
f.write('Patient Name = ' + patient.PatientName +'\n')
f.write('Patient ID = ' + patient.PatientID +'\n')
f.write('Planning Time = ' + time.strftime('%m-%d-%Y, %H:%M:%S',time.localtime(time.time())) +'\n')
f.write('Planning System = Topslane TPS 1.0.1978.138.V2.204161' +'\n')
f.write('Plan UID = '+ str(beamset.FrameOfReference) +'\n')
f.write('Plan Fraction = '+ str(beamset.FractionationPattern.NumberOfFractions) +'\n')

#Beams类型为ScriptObjectCollection,无法用len来获取计划射野个数
i=0
while 1:
    try:
        beam = beamset.Beams[i]
        i+=1
    except ValueError:
        break
beamnum=i
f.write('Total Beam Number = ' + str(beamnum) +'\n')
f.write('\n')
f.write('DMLC = Topslane_M (27 Pairs)' + '\n')
f.write('MLC Leaves Pair Number = 27' + '\n')
f.write('Max Overtravel Distance(cm) = 8.0' + '\n')
f.write('Source to MLC Top Edge Distance(cm) = 54.1' + '\n')
f.write('DoseRate = 0' + '\n')
f.write('\n')

for i in range(beamnum):
    f.write('Beam = Beam' + zfill(str(i+1),3) +'\n')
    f.write('Gantry Angle = ' + str(beamset.Beams[i].GantryAngle) + '\n')
    f.write('Collimator Angle = ' + str(beamset.Beams[i].InitialCollimatorAngle) + '\n')
    f.write('Turntable Angle = '+str(beamset.Beams[i].CouchAngle) + '\n')
    f.write('\n')
    
    #射野开口
    X1 = abs(round(beamset.Beams[i].Segments[0].JawPositions[0],1))
    X2 = abs(round(beamset.Beams[i].Segments[0].JawPositions[1],1))
    Y1 = abs(round(beamset.Beams[i].Segments[0].JawPositions[2],1))
    Y2 = abs(round(beamset.Beams[i].Segments[0].JawPositions[3],1))
    f.write('Fieldsize X(cm) = ' + str(X1+X2) + '\n')
    f.write('Fieldsize Y(cm) = ' + str(Y1+Y2) + '\n')
    f.write('Beam Jaw X1(cm) = ' + str(X1) + '\n')
    f.write('Beam Jaw X2(cm) = ' + str(X2) + '\n')
    f.write('Beam Jaw Y1(cm) = ' + str(Y1) + '\n')
    f.write('Beam Jaw Y2(cm) = ' + str(Y2) + '\n')  
    f.write('Machine Energy = ' + str(beamset.Beams[i].MachineReference.Energy) + '\n')
    f.write('Machine Name = Varian 600C-6MV' + '\n')
    f.write('Source Axis Distance(cm) = 100.00' +'\n')
    f.write('\n')
    
    #Segments类型为ScriptObjectCollection,无法用len来获取每个射野的子野个数
    j=0
    while 1:
        try:
            seg = beamset.Beams[i].Segments[j]
            j+=1
        except ValueError:
            break
    segnum=j
    f.write('Total Segment Number = ' + str(segnum) +'\n')
    f.write('\n')
    
    for j in range(segnum):
        f.write('Field No. = ' + str(segnum) + '-' + str(j+1) + '\n')
        f.write('Field MU = ' + str(round(beamset.Beams[i].BeamMU * beamset.Beams[i].Segments[j].RelativeWeight,1)) + '\n')
        f.write('MotorL = 24.95,  MotorR = 24.97' + '\n')
        #LeafPositions类型为Array，可用len
        for k in range(len(beamset.Beams[i].Segments[0].LeafPositions[0])):
            f.write('LeafL' + str(k) + ' = ' + str(round(beamset.Beams[i].Segments[0].LeafPositions[0][k],2)) 
              +',  LeafR' + str(k) + ' = ' + str(round(beamset.Beams[i].Segments[0].LeafPositions[1][k],2)) + '\n')
        f.write('\n')