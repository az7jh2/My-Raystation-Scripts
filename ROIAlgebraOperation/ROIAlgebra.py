# -*- coding: utf-8 -*-
#对ROI做环、添加其他辅助结构
#operation、sourcerouinames、marginsettings必不可少
#sourceroinames可只为一个
#Type: Expand or Contract
#Operation: Union or Intersection
#margin less than 15cm
#ResultOperation:None, Union, Intersection, Subtraction
#Created by Ningshan Li, 2015-7-7
#-------------------------------------------------------------------------#
from connect import *
#--------------------------------------------------------------------------#
#全局变量newrois
newrois=[]
deleterois=[]
#PTV收皮下0.3cm
def PTVinbody(patient,examination,roi,roiname,body,color):
    global newrois
    name=roiname+' in'
    patient.PatientModel.CreateRoi(Name=name,Color=color,Type='Ptv')
    roi[name].CreateAlgebraGeometry(Examination=examination,
      ExpressionA = { 'Operation': "Intersection", 'SourceRoiNames': 
      [roiname,body], 'MarginSettings': { 'Type': "Expand", 
      'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 
      'Right': 0, 'Left': 0 } },
      ResultOperation='None')
    newrois.append(name)
#---------------------------------------------------------------------------#
#做两个环
def tworings(patient,examination,roi,roiname,r1,r2,r3,color,body):
    global newrois,deleterois
    name1=roiname+'+'+str(r1)
    patient.PatientModel.CreateRoi(Name=name1,Type='Undefined')
    roi[name1].CreateMarginGeometry(Examination=examination,SourceRoiName=roiname,
      MarginSettings={ 'Type': "Expand", 'Superior' : r1, 'Inferior': r1, 
      'Anterior': r1, 'Posterior': r1, 'Right': r1, 'Left': r1 })
    
    name2=roiname+'+'+str(r2)
    patient.PatientModel.CreateRoi(Name=name2,Type='Undefined')
    roi[name2].CreateMarginGeometry(Examination=examination,SourceRoiName=roiname,
      MarginSettings={ 'Type': "Expand", 'Superior' : r2, 'Inferior': r2, 
      'Anterior': r2, 'Posterior': r2, 'Right': r2, 'Left': r2 })
    
    name3=roiname+'+'+str(r3)
    patient.PatientModel.CreateRoi(Name=name3,Type='Undefined')
    roi[name3].CreateMarginGeometry(Examination=examination,SourceRoiName=roiname,
      MarginSettings={ 'Type': "Expand", 'Superior' : r3, 'Inferior': r3, 
      'Anterior': r3, 'Posterior': r3, 'Right': r3, 'Left': r3 })
      
    ring1='ring1_'+roiname
    patient.PatientModel.CreateRoi(Name=ring1,Color=color[0],Type='Avoidance')
    roi[ring1].CreateAlgebraGeometry(Examination=examination,
      ExpressionA = { 'Operation': "Intersection", 'SourceRoiNames': 
      [name2,body], 'MarginSettings': { 'Type': "Expand", 
      'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 
      'Right': 0, 'Left': 0 } },
      ExpressionB = { 'Operation': "Intersection", 
      'SourceRoiNames': [name1,body], 'MarginSettings': { 
      'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 
      0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
      ResultOperation='Subtraction')
      
    ring2='ring2_'+roiname
    patient.PatientModel.CreateRoi(Name=ring2,Color=color[1],Type='Avoidance')
    roi[ring2].CreateAlgebraGeometry(Examination=examination,
      ExpressionA = { 'Operation': "Intersection", 'SourceRoiNames': 
      [name3,body], 'MarginSettings': { 'Type': "Expand", 
      'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 
      'Right': 0, 'Left': 0 } },
      ExpressionB = { 'Operation': "Intersection", 
      'SourceRoiNames': [name2,body], 'MarginSettings': { 
      'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 
      0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
      ResultOperation='Subtraction')

    newrois.extend([name1,name2,name3,ring1,ring2])
    deleterois.extend([name1,name2,name3])
#-----------------------------------------------------------------------#
#做三个环
def threerings(patient,examination,roi,roiname,r1,r2,r3,r4,color,body):
    global newrois,deleterois
    name1=roiname+'+'+str(r1)
    patient.PatientModel.CreateRoi(Name=name1,Type='Undefined')
    roi[name1].CreateMarginGeometry(Examination=examination,SourceRoiName=roiname,
      MarginSettings={ 'Type': "Expand", 'Superior' : r1, 'Inferior': r1, 
      'Anterior': r1, 'Posterior': r1, 'Right': r1, 'Left': r1 })
    
    name2=roiname+'+'+str(r2)
    patient.PatientModel.CreateRoi(Name=name2,Type='Undefined')
    roi[name2].CreateMarginGeometry(Examination=examination,SourceRoiName=roiname,
      MarginSettings={ 'Type': "Expand", 'Superior' : r2, 'Inferior': r2, 
      'Anterior': r2, 'Posterior': r2, 'Right': r2, 'Left': r2 })
    
    name3=roiname+'+'+str(r3)
    patient.PatientModel.CreateRoi(Name=name3,Type='Undefined')
    roi[name3].CreateMarginGeometry(Examination=examination,SourceRoiName=roiname,
      MarginSettings={ 'Type': "Expand", 'Superior' : r3, 'Inferior': r3, 
      'Anterior': r3, 'Posterior': r3, 'Right': r3, 'Left': r3 })
      
    name4=roiname+'+'+str(r4)
    patient.PatientModel.CreateRoi(Name=name4,Type='Undefined')
    roi[name4].CreateMarginGeometry(Examination=examination,SourceRoiName=roiname,
      MarginSettings={ 'Type': "Expand", 'Superior' : r4, 'Inferior': r4, 
      'Anterior': r4, 'Posterior': r4, 'Right': r4, 'Left': r4 })
    
    ring1='ring1_'+roiname
    patient.PatientModel.CreateRoi(Name=ring1,Color=color[0],Type='Avoidance')
    roi[ring1].CreateAlgebraGeometry(Examination=examination,
      ExpressionA = { 'Operation': "Intersection", 'SourceRoiNames': 
      [name2,body], 'MarginSettings': { 'Type': "Expand", 
      'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 
      'Right': 0, 'Left': 0 } },
      ExpressionB = { 'Operation': "Intersection", 
      'SourceRoiNames': [name1,body], 'MarginSettings': { 
      'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 
      0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
      ResultOperation='Subtraction')
      
    ring2='ring2_'+roiname
    patient.PatientModel.CreateRoi(Name=ring2,Color=color[1],Type='Avoidance')
    roi[ring2].CreateAlgebraGeometry(Examination=examination,
      ExpressionA = { 'Operation': "Intersection", 'SourceRoiNames': 
      [name3,body], 'MarginSettings': { 'Type': "Expand", 
      'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 
      'Right': 0, 'Left': 0 } },
      ExpressionB = { 'Operation': "Intersection", 
      'SourceRoiNames': [name2,body], 'MarginSettings': { 
      'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 
      0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
      ResultOperation='Subtraction')
    
    ring3='ring3_'+roiname
    patient.PatientModel.CreateRoi(Name=ring3,Color=color[2],Type='Avoidance')
    roi[ring3].CreateAlgebraGeometry(Examination=examination,
      ExpressionA = { 'Operation': "Intersection", 'SourceRoiNames': 
      [name4,body], 'MarginSettings': { 'Type': "Expand", 
      'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 
      'Right': 0, 'Left': 0 } },
      ExpressionB = { 'Operation': "Intersection", 
      'SourceRoiNames': [name3,body], 'MarginSettings': { 
      'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 
      0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
      ResultOperation='Subtraction')
    
    newrois.extend([name1,name2,name3,name4,ring1,ring2,ring3])
    deleterois.extend([name1,name2,name3,name4])
#-----------------------------------------------------------------------------#
#nt
def creatnt(patient,examination,roi,roiname,r1,color):
    global newrois
    PTV=roiname+'+'+str(r1)
    ring1='ring1_'+roiname
    ring2='ring2_'+roiname
    ring3='ring3_'+roiname
    patient.PatientModel.CreateRoi(Name='nt',Color=color,Type='Undefined')
    roi['nt'].CreateAlgebraGeometry(Examination=examination,
      ExpressionA = { 'Operation': "Union", 'SourceRoiNames': 
      ['Bodys'], 'MarginSettings': { 'Type': "Expand", 
      'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 
      'Right': 0, 'Left': 0 } },
      ExpressionB = { 'Operation': "Union", 
      'SourceRoiNames': [PTV,ring1,ring2,ring3], 'MarginSettings': { 
      'Type': "Contract", 'Superior': 0, 'Inferior': 0, 'Anterior': 
      0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
      ResultOperation='Subtraction')
      
    newrois.append('nt')
#------------------------------------------------------------------------------#
#Body，缩小的外轮廓
def creatbodys(patient,examination,roi,roiname,r1,r2,color):
    global newrois,deleterois
    
    patient.PatientModel.CreateRoi(Name='temp0',Type='Undefined')
    roi['temp0'].CreateMarginGeometry(Examination=examination,SourceRoiName=roiname,
        MarginSettings={ 'Type': "Expand", 'Superior' : 0, 'Inferior': 0, 
        'Anterior': 5, 'Posterior': 5, 'Right': 5, 'Left': 5 })
    
    patient.PatientModel.CreateRoi(Name='temp1',Type='Undefined')
    roi['temp1'].CreateMarginGeometry(Examination=examination,SourceRoiName='temp0',
        MarginSettings={ 'Type': "Expand", 'Superior' : 0, 'Inferior': 0, 
        'Anterior': 5, 'Posterior': 5, 'Right': 5, 'Left': 5 })
        
    patient.PatientModel.CreateRoi(Name='temp2',Type='Undefined')
    roi['temp2'].CreateMarginGeometry(Examination=examination,SourceRoiName='temp1',
        MarginSettings={ 'Type': "Expand", 'Superior' : 0, 'Inferior': 0, 
        'Anterior': 5, 'Posterior': 5, 'Right': 5, 'Left': 5 })
        
    patient.PatientModel.CreateRoi(Name='Bodys',Color=color,Type='Undefined')
    roi['Bodys'].CreateAlgebraGeometry(Examination=examination,
      ExpressionA = { 'Operation': "Union", 'SourceRoiNames': 
      ['temp2'], 'MarginSettings': { 'Type': "Expand", 
      'Superior': r1, 'Inferior': r1, 'Anterior': 5, 'Posterior': 5, 
      'Right': 5, 'Left': 5 } },
      ExpressionB = { 'Operation': "Union", 
      'SourceRoiNames': ['External'], 'MarginSettings': { 
      'Type': "Contract", 'Superior': 0, 'Inferior': 0, 'Anterior': 
      0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
      ResultOperation='Intersection')
      
    newrois.append('Bodys')
    deleterois.extend(['temp0','temp1','temp2'])
#------------------------------------------------------------------------------#
#PTV收皮下,创建皮下一定距离ROI
def bodycontract(patient,examination,roi,r,color):
    global newrois
    name='Bodys-'+str(r)
    patient.PatientModel.CreateRoi(Name=name,Color=color,Type='Undefined')      
    roi[name].CreateMarginGeometry(Examination=examination,SourceRoiName='Bodys',
      MarginSettings={ 'Type': "Contract", 'Superior' : 0.0, 'Inferior': 0.0, 
      'Anterior': r, 'Posterior': r, 'Right': r, 'Left': r })
      
    newrois.append(name)
#------------------------------------------------------------------------------#
#低剂量PTV剪高剂量PTV,A为高剂量，B为低剂量
def PTVconsubtract(patient,examination,roi,roiAname,roiBname,r,color):
    global newrois
    Aname=roiAname+'+'+str(r)
    Bname=roiBname+' opt'
    rois=[]
    for rg in patient.PatientModel.StructureSets[examination.Name].RoiGeometries:
        rois.append(rg.OfRoi.Name)
    patient.PatientModel.CreateRoi(Name=Bname,Color=color,Type='Ptv')
    if Aname in rois:
        roi[Bname].CreateAlgebraGeometry(Examination=examination,
          ExpressionA = { 'Operation': "Union", 'SourceRoiNames': 
          [roiBname], 'MarginSettings': { 'Type': "Expand", 
          'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 
          'Right': 0, 'Left': 0 } },
          ExpressionB = { 'Operation': "Union", 
          'SourceRoiNames': [Aname], 'MarginSettings': { 
          'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 
          0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
          ResultOperation='Subtraction')
    else:
        roi[Bname].CreateAlgebraGeometry(Examination=examination,
          ExpressionA = { 'Operation': "Union", 'SourceRoiNames': 
          [roiBname], 'MarginSettings': { 'Type': "Expand", 
          'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 
          'Right': 0, 'Left': 0 } },
          ExpressionB = { 'Operation': "Union", 
          'SourceRoiNames': [roiAname], 'MarginSettings': { 
          'Type': "Expand", 'Superior': r, 'Inferior': r, 'Anterior': 
          r, 'Posterior': r, 'Right': r, 'Left': r } },
          ResultOperation='Subtraction')
          
    newrois.append(Bname)
#-------------------------------------------------------------------------#
#除去体积小的轮廓
def fixroi(structure_set,roinames,r):
    structure_set.SimplifyContours(RoiNames=roinames, RemoveHoles3D=False, RemoveSmallContours=True, AreaThreshold=r,
      ReduceMaxNumberOfPointsInContours=False, MaxNumberOfPoints=None, CreateCopyOfRoi=False)
#-----------------------------------------------------------------------------#
#主程序
def main(ROI):
    patient=get_current('Patient')
    examination=get_current('Examination')
    structure_set=patient.PatientModel.StructureSets[examination.Name]
    roi=patient.PatientModel.RegionsOfInterest

#判断所需的ROI是否存在
    roilist=[]
    for rg in structure_set.RoiGeometries:
        roilist.append(rg.OfRoi.Name)
    for i in ROI:
        if not(i in roilist):
            raise RuntimeError(i+' is not exist')

#Body，缩小的外轮廓
    creatbodys(patient,examination,roi,ROI[2],2,20,'Green')

#PTV收皮下0.3cm
    bodycontract(patient,examination,roi,0.3,'Blue')

    PTVinbody(patient,examination,roi,ROI[0],'Bodys-0.3','Orange')
    PTVinbody(patient,examination,roi,ROI[1],'Bodys-0.3','Brown')
    PTVinbody(patient,examination,roi,ROI[2],'Bodys-0.3','Blue')

#PTV做环,并收皮下
    tworings(patient,examination,roi,'PGTV in',0.3,0.8,1.8,['Green','Pink'],'Bodys-0.3')
    tworings(patient,examination,roi,'PCTV1 in',0.3,0.8,1.8,['Yellow','Purple'],'Bodys-0.3')
    threerings(patient,examination,roi,'PCTV2 in',0.3,0.8,1.8,3.3,['Green','Pink','Purple'],'Bodys-0.3')

#nt
    creatnt(patient,examination,roi,'PCTV2 in',0.3,'Gray')

#低剂量PTV剪高剂量PTV，第一个为高剂量，第二个为低剂量
    PTVconsubtract(patient,examination,roi,'PGTV in','PCTV1 in',0.3,'Black')
    PTVconsubtract(patient,examination,roi,'PCTV1 in','PCTV2 in',0.3,'Red')

#去除新生成ROI的小体积
    global newrois
    fixroi(structure_set,newrois,0.1)
    
    #删除中间ROI
    global deleterois
    for i in deleterois:
        roi[i].DeleteRoi()
    
#-----------------------------------------------------------------------------#
if __name__=='__main__':
    main(['PGTV','PCTV1','PCTV2','External']) 