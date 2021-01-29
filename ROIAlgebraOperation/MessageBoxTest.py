from connect import *
import ctypes

#-----------------------------------------------------------------
def Mbox(title, text, style):
	ctypes.windll.user32.MessageBoxW(0, text, title, style)
#-----------------------------------------------------------------
Mbox('Warning' , 'This is a test of MessageBox' , 0)
print 'this statement is still executed' 