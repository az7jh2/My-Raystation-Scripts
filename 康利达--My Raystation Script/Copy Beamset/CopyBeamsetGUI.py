# -*- coding: utf-8 -*-
#GUI for Copybeamset
#created by Ningshan Li 2015-6-23 
from connect import *

import wpf
from System.Windows import *
from System.Windows.Controls import *

import clr
clr.AddReference("System.Core")
import System
clr.ImportExtensions(System.Linq)

import CopyBeamset_V4

import ctypes
#-----------------------------------------------------------------
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxW(0, text, title, style)
#---------------------------------------------------------------------------------------------------#
    
class MainWindow(Window):

  # Eventhandler
  def button_clicked(self, sender, event):
    self.selected_plan = self.cbPlans.SelectedItem
    self.selected_beamset = self.cbBeamsets.SelectedItem
    self.selected_FromCT = self.cbFromCT.SelectedItem
    self.selected_ToCT = self.cbToCT.SelectedItem
    self.selected_mode = self.cbMode.SelectedItem
    self.selected_newplanname=self.newplantext.Text
    self.selected_newbeamsetname=self.newbeamsettext.Text
    
    if self.selected_plan==None:
        Mbox('Warning','No plan is selected',0)
        return
    if self.selected_beamset==None:
        Mbox('Warning','No beamset is selected',0)
        return
    if self.selected_FromCT==None:
        Mbox('Warning','No From exmination is selected',0)
        return
    if self.selected_ToCT==None:
        Mbox('Warning','No To exmination is selected',0)
        return
    if self.selected_mode==None:
        Mbox('Warning','No copy mode is selected',0)
        return
    if self.selected_newplanname=='':
        Mbox('Warning','The inputed new name of plan is empty',0)
        return
    if self.selected_newbeamsetname=='':
        Mbox('Warning','The inputed new name of beamset is empty',0)
        return
    
    self.lResult.Text ='Copy performing. Please wait...'
    self.lResult.Visibility=Visibility.Visible
    
    r=CopyBeamset_V4.main(planname=self.selected_plan,beamsetname=self.selected_beamset,fromexamname=self.selected_FromCT,
      toexamname=self.selected_ToCT,mode=self.selected_mode,newplanname=self.selected_newplanname,newbeamsetname=self.selected_newbeamsetname)
    
    if r==0:
        self.lResult.Text ='Copy failed'
    elif r==1:
        self.lResult.Text ='Copy completed'
  
  def close_clicked(self,sender,event):
      self.DialogResult=True
      
  def __init__(self, title, imagesets, plans,beamsets,modes):
    
    wpf.LoadComponent(self, 'CopyBeamset.xaml')

    self.Title = title

    self.cbPlans.ItemsSource = plans
    self.cbBeamsets.ItemsSource = beamsets
    self.cbFromCT.ItemsSource = imagesets
    self.cbToCT.ItemsSource = imagesets
    self.cbMode.ItemsSource = modes
#####################################
patient = get_current("Patient")

imagesets = []
for examination in patient.Examinations:
    imagesets.Add(examination.Name)

plans = []
beamsets=[]
for plan in patient.TreatmentPlans:
    plans.Add(plan.Name)
    for beamset in plan.BeamSets:
        beamsets.Add(beamset.DicomPlanLabel)
modes=['Copy from prototype','Zeros','Rigid Registration']
        
dialog = MainWindow("Copy Beamset",imagesets,plans,beamsets,modes)
dialog.ShowDialog()
