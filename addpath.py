# -*- coding: utf-8 -*-
#将路径加入path,每次退出python环境，路径会失效
import sys
sys.path.append('C:\\Program Files\\RaySearch Laboratories\\RayStation 4.5.1\\ScriptClient')
sys.path.append('D:\\hill103\\Script\\Get Control Point')
sys.path.append('E:\\Script\\Plan Evaluation')
sys.path.append('E:\\Script\\DICOM Rename')

import os
os.chdir('E:\\Script\\DICOM Rename\\pydicom-0.9.9')
python setup.py install
