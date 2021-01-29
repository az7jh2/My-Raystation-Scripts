connect_ok = True
try:
  from connect import *
except:
  connect_ok = False

import wpf
from System import (DateTime, Windows, Globalization)


import clr
clr.AddReference("System.Core")
import System
clr.ImportExtensions(System.Linq)

class MeasurementWindow(Windows.Window):

  # Eventhandler
  def OnDropDownImageSetsClosed(self, sender, event):
    if self.cbImageSets.SelectedItem == 0 or self.cbImageSets.SelectedItem != self.selected_image_set:
      self.lVolA.Content = ""
      self.lVolB.Content = ""
      self.lDice.Content = ""
      self.lPrec.Content = ""
      self.lSens.Content = ""
      self.lSpec.Content = ""

 
  # Eventhandler
  def compute_clicked(self, sender, event):
    self.selected_image_set = self.cbImageSets.SelectedItem
    self.selected_roi_a = self.cbRoiA.SelectedItem
    self.selected_roi_b = self.cbRoiB.SelectedItem

    structureSet=patient.PatientModel.StructureSets[self.selected_image_set]

    rgA = structureSet.RoiGeometries[self.selected_roi_a]
    rgB = structureSet.RoiGeometries[self.selected_roi_b]

    measures = structureSet.ComparisonOfRoiGeometries(RoiA = self.selected_roi_a, RoiB = self.selected_roi_b)
    
    self.lRoiA.Content = self.selected_roi_a
    self.lRoiB.Content = self.selected_roi_b

    self.lVolA.Content = "{0:.2F}".format(rgA.GetRoiVolume())
    self.lVolB.Content = "{0:.2F}".format(rgB.GetRoiVolume())

    comA = rgA.GetCenterOfRoi()
    comB = rgB.GetCenterOfRoi()

    self.lComA.Content = "({0:.2F},{1:.2F},{2:.2F})".format(comA.x,comA.y, comA.z)
    self.lComB.Content = "({0:.2F},{1:.2F},{2:.2F})".format(comB.x,comB.y, comB.z)

    self.lDice.Content = "{0:.3F}".format(measures["Dice similarity index"])
    self.lPrec.Content = "{0:.3F}".format(measures["Precision"])
    self.lSens.Content = "{0:.3F}".format(measures["Sensitivity"])
    self.lSpec.Content = "{0:.3F}".format(measures["Specificity"])

  def __init__(self, title, imagesets, roigeometries):
    
    wpf.LoadComponent(self, "D:\\hill103\\Script\\XAML for Reference\\roi_comparison.xaml")

    self.Title = title

    self.cbImageSets.ItemsSource = imagesets
    self.cbRoiA.ItemsSource = roigeometries
    self.cbRoiB.ItemsSource = roigeometries
    self.selected_image_set = 0

    self.bCompute.Click += self.compute_clicked



class RoiComparison:
  def __init__(roiA, roiB, volumeA, volumeB, dice, precision):
    self.roiA = roiA
    self.roiB = roiB
    self.volumeA = volumeA
    self.volumeB = volumeB
    self.dice = dice
    self.precision = precision

#####################################

if connect_ok:
  patient = get_current("Patient")

  imagesets = []
  for examination in patient.Examinations:
    imagesets.Add(examination.Name)

  roigeometries = []
  for rg in patient.PatientModel.RegionsOfInterest:
    roigeometries.Add(rg.Name)
    
  dialog = MeasurementWindow("ROI comparison",imagesets, roigeometries)
  dialog.ShowDialog()