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
#创建ROI，若有重名，则删除原有的ROI
def creatroi(patient,roi,name,color='Blue',ty='Undefined'):
    try:
        patient.PatientModel.CreateRoi(Name=name,Color=color,Type=ty)
    except:
        roi[name].DeleteRoi()
        patient.PatientModel.CreateRoi(Name=name,Color=color,Type=ty)
#----------------------------------------------------------------------------#
#PTV收皮下0.3cm
def PTVinbody(patient,examination,roi,roiname,body,color):
    global newrois
    name=roiname+' in'
    creatroi(patient,roi,name,color,'Ptv')
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
    creatroi(patient,roi,name1)
    roi[name1].CreateMarginGeometry(Examination=examination,SourceRoiName=roiname,
      MarginSettings={ 'Type': "Expand", 'Superior' : r1, 'Inferior': r1, 
      'Anterior': r1, 'Posterior': r1, 'Right': r1, 'Left': r1 })
    
    name2=roiname+'+'+str(r2)
    creatroi(patient,roi,name2)
    roi[name2].CreateMarginGeometry(Examination=examination,SourceRoiName=roiname,
      MarginSettings={ 'Type': "Expand", 'Superior' : r2, 'Inferior': r2, 
      'Anterior': r2, 'Posterior': r2, 'Right': r2, 'Left': r2 })
    
    name3=roiname+'+'+str(r3)
    creatroi(patient,roi,name3)
    roi[name3].CreateMarginGeometry(Examination=examination,SourceRoiName=roiname,
      MarginSettings={ 'Type': "Expand", 'Superior' : r3, 'Inferior': r3, 
      'Anterior': r3, 'Posterior': r3, 'Right': r3, 'Left': r3 })
      
    ring1='ring1_'+roiname
    creatroi(patient,roi,ring1,color[0],'Avoidance')
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
    creatroi(patient,roi,ring2,color[1],'Avoidance')
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
    creatroi(patient,roi,name1)
    roi[name1].CreateMarginGeometry(Examination=examination,SourceRoiName=roiname,
      MarginSettings={ 'Type': "Expand", 'Superior' : r1, 'Inferior': r1, 
      'Anterior': r1, 'Posterior': r1, 'Right': r1, 'Left': r1 })
    
    name2=roiname+'+'+str(r2)
    creatroi(patient,roi,name2)
    roi[name2].CreateMarginGeometry(Examination=examination,SourceRoiName=roiname,
      MarginSettings={ 'Type': "Expand", 'Superior' : r2, 'Inferior': r2, 
      'Anterior': r2, 'Posterior': r2, 'Right': r2, 'Left': r2 })
    
    name3=roiname+'+'+str(r3)
    creatroi(patient,roi,name3)
    roi[name3].CreateMarginGeometry(Examination=examination,SourceRoiName=roiname,
      MarginSettings={ 'Type': "Expand", 'Superior' : r3, 'Inferior': r3, 
      'Anterior': r3, 'Posterior': r3, 'Right': r3, 'Left': r3 })
      
    name4=roiname+'+'+str(r4)
    creatroi(patient,roi,name4)
    roi[name4].CreateMarginGeometry(Examination=examination,SourceRoiName=roiname,
      MarginSettings={ 'Type': "Expand", 'Superior' : r4, 'Inferior': r4, 
      'Anterior': r4, 'Posterior': r4, 'Right': r4, 'Left': r4 })
    
    ring1='ring1_'+roiname
    creatroi(patient,roi,ring1,color[0],'Avoidance')
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
    creatroi(patient,roi,ring2,color[1],'Avoidance')
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
    creatroi(patient,roi,ring3,color[2],'Avoidance')
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
    creatroi(patient,roi,'nt',color,'Avoidance')
    roi['nt'].CreateAlgebraGeometry(Examination=examination,
      ExpressionA = { 'Operation': "Union", 'SourceRoiNames': 
      ['Bodys-0.3'], 'MarginSettings': { 'Type': "Expand", 
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
#Copy ROI无法Scripting
def creatbodys(patient,examination,roi,roiname,externalname,color):
    global newrois,deleterois
    #获取Z-range
    roigeo=patient.PatientModel.StructureSets[examination.Name].RoiGeometries[roiname]
    [zmin,zmax]=zrange(roigeo)
    
    externalgeo=patient.PatientModel.StructureSets[examination.Name].RoiGeometries[externalname]
    [size,center]=boxsize(externalgeo,zmin,zmax)
    
    creatroi(patient,roi,'Box')
    roi['Box'].CreateBoxGeometry(Size =  size , Examination = examination , Center = center)
    
    creatroi(patient,roi,'Bodys',color)
    roi['Bodys'].CreateAlgebraGeometry(Examination=examination,
          ExpressionA = { 'Operation': "Union", 'SourceRoiNames': 
          ['Box'], 'MarginSettings': { 'Type': "Expand", 
          'Superior': 0, 'Inferior': 0, 'Anterior': 0, 'Posterior': 0, 
          'Right': 0, 'Left': 0 } },
          ExpressionB = { 'Operation': "Union", 
          'SourceRoiNames': [externalname], 'MarginSettings': { 
          'Type': "Expand", 'Superior': 0, 'Inferior': 0, 'Anterior': 
          0, 'Posterior': 0, 'Right': 0, 'Left': 0 } },
          ResultOperation='Intersection')
      
    newrois.append('Bodys')
    deleterois.extend(['Box'])
#------------------------------------------------------------------------------#
#获取ROI的z-range
def zrange(roigeometry):
    bbox = roigeometry.GetBoundingBox()
    if bbox.Count==2:
        return bbox[0].z,bbox[1].z
    else:
        raise Exception('The length of BoundingBox is not equal 2')
#------------------------------------------------------------------------------#
def boxsize(roigeometry,zmin,zmax):
    bbox = roigeometry.GetBoundingBox()
    if bbox.Count==2:
        xsize = bbox[1].x - bbox[0].x + 2.0
        ysize = bbox[1].y - bbox[0].y + 2.0
        zsize = abs(zmax - zmin) + 2.0
        xcenter=roigeometry.GetCenterOfRoi().x
        ycenter=roigeometry.GetCenterOfRoi().y
        zcenter=zmin+(zmax-zmin)/2
        size = {"x":xsize , "y": ysize, "z":zsize}
        center = {"x":xcenter, "y":ycenter, "z":zcenter}
        return size,center
    else:
        raise Exception('The length of BoundingBox is not equal 2')
#--------------------------------------------------------------------------------#
#PTV收皮下,创建皮下一定距离ROI
def bodycontract(patient,examination,roi,r,color):
    global newrois
    name='Bodys-'+str(r)
    creatroi(patient,roi,name,color)      
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
    creatroi(patient,roi,Bname,color,'Ptv')
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
            raise Exception('ROI {0} is not exist'.format(i))

#寻找外轮廓
    try:
        external_roi = next(r for r in roi if r.Type == 'External')
    except:
        raise Exception('No external ROI defined')
    extername=external_roi.Name

#Body，缩小的外轮廓
    creatbodys(patient,examination,roi,ROI[2],extername,'Green')

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
    main(['PGTV','PCTV1','PCTV2']) 