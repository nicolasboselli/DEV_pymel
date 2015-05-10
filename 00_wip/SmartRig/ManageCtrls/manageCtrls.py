'''
Created on 6 mai 2015

@author: nicolas_2
'''

# Import PySide classes
import cleanPipeline.cleanModules as clean
clean.cleanModules()

import sys


import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import pymel.core as pm
import maya.mel as mm
import SmartRig.createHelpers as helpers
import SmartRig.IKFK.FK_chain as FK
import SmartRig.ManageCtrls.manageCtrls_def as MC

try:
    import sip
    
    from PyQt4 import QtCore
    from PyQt4 import QtGui
    
    def maya_main_window():
        ptr = omui.MQtUtil.mainWindow()
        if ptr is not None:
            return sip.wrapinstance(long(ptr), QtCore.QObject)
    print('import 2012')
        
except Exception as ex:
    from shiboken import wrapInstance
    
    from PySide import QtCore
    from PySide import QtGui
    
    def maya_main_window():
        main_window_ptr = omui.MQtUtil_mainWindow()
        return wrapInstance(long(main_window_ptr), QtGui.QWidget)
    om.MGlobal_displayInfo('import 2014')
    
from SmartRig.ManageCtrls.manageCtrls_ui import Ui_Form

class ManageCtrls(QtGui.QDialog):
    def __init__(self, parent = None):
        super(ManageCtrls, self).__init__(parent = maya_main_window())
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setupConnections()
#         self.initUi()
    def setupConnections(self):
        self.ui.Xminus_pb.clicked.connect(self.moveXminus)
        self.ui.Xplus_pb.clicked.connect(self.moveXplus)
        
    def moveXplus(self):
        sel = pm.ls(sl = True)
        for s in sel:
            MC.moveShape(s, movX = True, move = 1)
    def moveXminus(self):
        sel = pm.ls(sl = True)
        for s in sel:
            MC.moveShape(s, movX = True, move = -1)
            
        
ManageCtrlUI = ManageCtrls()
ManageCtrlUI.show()
#ui.close()
print('done')