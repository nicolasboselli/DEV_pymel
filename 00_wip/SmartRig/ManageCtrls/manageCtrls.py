'''
Created on 6 mai 2015

@author: nicolas_2
'''

# Import PySide classes
import cleanPipeline.cleanModules as clean
clean.cleanModules()

"""
maj: 
-- keep selection after action
-- add scale parameters
"""


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
        
        self.ui.Yminus_pb.clicked.connect(self.moveYminus)
        self.ui.Yplus_pb.clicked.connect(self.moveYplus)

        self.ui.Zminus_pb.clicked.connect(self.moveZminus)
        self.ui.Zplus_pb.clicked.connect(self.moveZplus)
        
        
        self.ui.scaleXYZ_minus_pb.clicked.connect(self.scaleXYZminus)
        self.ui.scaleXYZ_plus_pb.clicked.connect(self.scaleXYZplus)
        
        self.ui.scaleX_minus_pb.clicked.connect(self.scaleXminus)
        self.ui.scaleX_plus_pb.clicked.connect(self.scaleXplus)
        
        self.ui.scaleY_minus_pb.clicked.connect(self.scaleYminus)
        self.ui.scaleY_plus_pb.clicked.connect(self.scaleYplus)
        
        self.ui.scaleZ_minus_pb.clicked.connect(self.scaleZminus)
        self.ui.scaleZ_plus_pb.clicked.connect(self.scaleZplus)
        
        
    def moveXminus(self):
        sel = pm.ls(sl = True)
        for s in sel:
            MC.moveShape(s, movX = True, move = -1)
        pm.select(sel)
            
    def moveXplus(self):
        sel = pm.ls(sl = True)
        for s in sel:
            MC.moveShape(s, movX = True, move = 1)
        pm.select(sel)
    
    def moveYminus(self):
        sel = pm.ls(sl = True)
        for s in sel:
            MC.moveShape(s, movY = True, move = -1)
        pm.select(sel)
            
    def moveYplus(self):
        sel = pm.ls(sl = True)
        for s in sel:
            MC.moveShape(s, movY = True, move = 1)
        pm.select(sel)

    def moveZminus(self):
        sel = pm.ls(sl = True)
        for s in sel:
            MC.moveShape(s, movZ = True, move = -1)
        pm.select(sel)
            
    def moveZplus(self):
        sel = pm.ls(sl = True)
        for s in sel:
            MC.moveShape(s, movZ = True, move = 1)
        pm.select(sel)
    
    def scaleXYZminus(self):
        sel = pm.ls(sl = True)
        for s in sel:
            MC.scaleShape(s, scale = 0.5)
        pm.select(sel)
            
    def scaleXYZplus(self):
        sel = pm.ls(sl = True)
        for s in sel:
            MC.scaleShape(s, scale = 2)
        pm.select(sel)
    
    def scaleXminus(self):
        sel = pm.ls(sl = True)
        for s in sel:
            MC.scaleShape(s, scalX = True, scale = 0.5)
        pm.select(sel)
            
    def scaleXplus(self):
        sel = pm.ls(sl = True)
        for s in sel:
            MC.scaleShape(s, scalX = True, scale = 2)
        pm.select(sel)
            
    def scaleYminus(self):
        sel = pm.ls(sl = True)
        for s in sel:
            MC.scaleShape(s, scalY = True, scale = 0.5)
        pm.select(sel)
            
    def scaleYplus(self):
        sel = pm.ls(sl = True)
        for s in sel:
            MC.scaleShape(s, scalY = True, scale = 2)
        pm.select(sel)
            
    def scaleZminus(self):
        sel = pm.ls(sl = True)
        for s in sel:
            MC.scaleShape(s, scalZ = True, scale = 0.5)
        pm.select(sel)
            
    def scaleZplus(self):
        sel = pm.ls(sl = True)
        for s in sel:
            MC.scaleShape(s, scalZ = True, scale = 2)
        pm.select(sel)
    

            
        
ManageCtrlUI = ManageCtrls()
ManageCtrlUI.show()
#ui.close()
print('done')