#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

'''
Created on 22 May 2014

@author: nboselli
'''

#TODO: cleaning module scripts
"""
debug:
    create two controllers on the same joint(delete old system, implement?)
    create two alias on the same joint(delete old system, implement?)
    recreate hierarchy with alias:
        on each alias creation find alias position in hierarchy and place it?
"""



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

from SmartRig.MyMayaScripts.UI_myMayaScripts import Ui_Dialog
import SmartRig.jointsMisc as jointsDef
import SmartRig.colorControl as color
import SmartRig.makeRibbon as ribbon
import SmartRig.createHelpers as shapes

import SmartRig.IKFK as ikfk


class MyCompanion(QtGui.QDialog):
    
    def __init__(self, parent = None):
        super(MyCompanion, self).__init__(parent = maya_main_window())
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setupConnections()
        self.initUi()
        
        #self.setWindowTitle("Primitive")
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    
    def initUi(self):
        self.ui.helpTool_arrowL_tb.setVisible(False)
        self.ui.jointTool_arrowL_tb.setVisible(False)
        self.ui.ikTool_arrowL_tb.setVisible(False)
    
    def setupConnections(self):
#         circle connection
#         maj: clone hierarchy, add parent constraint, add scale constraint
        self.ui.circleX_pb.clicked.connect(lambda: helpers.createCircle([1,0,0]))
        self.ui.circleY_pb.clicked.connect(lambda: helpers.createCircle([0,1,0]))
        self.ui.circleZ_pb.clicked.connect(lambda: helpers.createCircle([0,0,1]))
        
# alias connection
        self.ui.createAlias_pb.clicked.connect(self.createAlias)
        
#         locators connection
        self.ui.loc10_pb.clicked.connect(lambda: helpers.createLoc(1))
        self.ui.loc05_pb.clicked.connect(lambda: helpers.createLoc(0.5))
        self.ui.loc02_pb.clicked.connect(lambda: helpers.createLoc(0.2))
        
#         parent connection
        self.ui.rootGrp_pb.clicked.connect(helpers.rootGroup)
        self.ui.insertGrp_pb.clicked.connect(helpers.insertGroups)
        self.ui.childGrp_pb.clicked.connect(helpers.childGroup)
        
#         colors assignement
        self.ui.yellow_pb.clicked.connect(lambda: color.colored(17))
        self.ui.red_pb.clicked.connect(lambda: color.colored(13))
        self.ui.blue_pb.clicked.connect(lambda: color.colored(6))
        
#         controller Shapes
        self.ui.ctrlCube_pb.clicked.connect(shapes.createOneCube)
        
#         joints connection
        self.ui.resizeJoint_pb.clicked.connect(self.resizeJoints)

        self.ui.hideJoint_pb.clicked.connect(jointsDef.hideJoints)
        self.ui.showJoints_pb.clicked.connect(jointsDef.showJoints)
        self.ui.showOrient_pb.clicked.connect(jointsDef.displayJointOrient)
        
        self.ui.hideOrient_pb.clicked.connect(lambda: jointsDef.displayJointOrient(0))
        self.ui.freezeOrient_pb.clicked.connect(jointsDef.freezeJoint)
        
        self.ui.lraOn_pb.clicked.connect(lambda: jointsDef.displayLocalAxis(1))
        self.ui.lraOff_pb.clicked.connect(jointsDef.displayLocalAxis)
        
#         dist connect
        self.ui.dim_pb.clicked.connect(helpers.creatDist)
        
#         ribbon
        self.ui.plane_pb.clicked.connect(ribbon.createPlane)
        self.ui.ribbon_pb.clicked.connect(ribbon.makeRibbon)
        
#         ik spline
        self.ui.arc_pb.clicked.connect(self.createArcPart)   
        
#         FK     
        self.ui.createFK_pb.clicked.connect(self.createFK)
        
#         IKFK members
        self.ui.ikfk_pb.clicked.connect(self.createIKFK)
        
#         create reverse foot
        self.ui.revFoot_pb.clicked.connect(self.createRevFoot)
        
#         IKFK spline
        self.ui.revFoot_pb.clicked.connect(self.createIKFKspline)
    
    def createAlias(self):
        sel = pm.ls(sl = True)
        for s in sel:
            helpers.createOneAlias(s)
        print "alias created"
        
    def createFK(self):
        sel = pm.ls(sl = True)
        hierarchyState = self.ui.selectHierarchy_cb.isChecked()
        anchorState = self.ui.FKanchor_cb.isChecked()
        FK.createFKchain(sel = sel, collectHierarchy = hierarchyState, linkChain = anchorState )
        
    def createIKFK(self):
        sel = pm.ls(sl = True)
        
        
    def createRevFoot(self):
        sel = pm.ls(sl = True)
        
    def createIKFKspline(self):
        sel = pm.ls(sl = True)
    
    def testButton(self):
        print('test')
    
    def createArcPart(self):
        pass
        
    def resizeJoints(self):
        print 'resize powa!'
        size = self.ui.jointSize_sb.value()
        if self.ui.jointSizeSel_rb1.isChecked():
            print'on selection'
            jointsDef.resizeJoints(jointSize= size, all = False)
        elif self.ui.jointSizeSel_rb2.isChecked():
            print 'on all'
            jointsDef.resizeJoints(jointSize= size, all = True)
        
    
MyMayaScriptsUI = MyCompanion()
MyMayaScriptsUI.show()
#ui.close()
print('done')

