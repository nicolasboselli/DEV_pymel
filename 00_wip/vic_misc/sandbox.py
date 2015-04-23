

import os, sys

smartRig = r'C:\Users\Gamma Project\Documents\maya\scripts'
sys.path.append(smartRig)

import maya.mel as mel

from PySide import QtCore
from PySide import QtGui
import pymel.core as pm

from SmartRig.UI_hideJoint import Ui_Dialog as UI
# reload(UI_hideJoint)

from pprint import pprint

# find mesh with multiple shader
def findMultiMat():
    meshes = pm.ls(type = 'shape')
    # 
    for m in meshes:
        shader = pm.listConnections(m, type = 'shadingEngine')
        if len(shader)>2:
            print(m)

# add msh name
def addMsh():
    sel = pm.ls(sl = True)
     
    for s in sel:
        oldName = s.name()
        newName = oldName + '_msh'
        print(s.rename(newName))
     
def selectMesh():
    sel = []      
    for sl in pm.ls(sl = True):
        print(sl)
        shps = []
        shps = pm.listRelatives(sl, allDescendents  = True, shapes = True, noIntermediate = True)
        pprint(shps)
        for shp in shps:
            print(pm.objectType(shp))
            if pm.objectType(shp) == 'mesh':
                tr = pm.listRelatives(shp, parent = True, path = True)
                for t in tr:
                    if t not in sel:
                        sel.append(t)
    
    pprint(sel)
#     pm.select(sel)
    return sel

# sel = selectMesh()
# pm.select(sel)


# # reorient joint
# sel = pm.ls(sl = True)[0]
# # pm.rotate(relative  = True, objectSpace  = True, (180, 0 , 180))
# joints = pm.listRelatives(sel, allDescendents = True, path = True)
# joints.append(sel)
# pprint(joints)
# 
# for j in joints:
#     pm.parent(j, w = True)
#     pm.select(j)
#     pm.rotate(180, 180 , 0 ,r = True, os = True)
# #     pm.rotate(0, 180 , 0 ,r = True, os = True)
# #     pm.rotate(0, 0 , '180deg' ,r = True, os = True)
# 
# 
# for i in range(0,(len(joints)-1)):
#     pm.parent(joints[i], joints[i+1])
    
# copy one skincluster to objects selection
source = 'model1:body_msh'
# source = 'model1:hairStrand1_msh'
   
targets = pm.ls(sl = True)
pprint(targets)
   
for t in targets:
    pm.select( clear = True)
    pm.select(source)
    pm.select(t, add = True)
   
    mel.eval('qa_matchInfluences')
    mel.eval('qa_launchMayaCopySkinWeightsBtwn2Objs')


# sel = ['model:vic___original', 'model1:model_grp' ]
# meshesList = []
# for s in sel:
#     pm.select(s)
#     list = selectMesh()
#     meshesList.append(list)
# 
# for source in meshesList[0]:
#     for target in meshesList[1]:
#         sName = (source.name()).split(':')[-1]
#         tName = (target.name()).split(':')[-1]
#         if sName == tName:
#             print(source, target)
#             pm.select(source, target)
#             mel.eval('qa_matchInfluences')
#             mel.eval('qa_launchMayaCopySkinWeightsBtwn2Objs')

# hide all joints local axis
def hideAllJointsRLA():
    joints = pm.ls(type = 'joint')
    pprint(joints)
    
    for j in joints:
        pm.setAttr('%s.displayLocalAxis' % j, False)

# meshes = selectMesh()
# pm.select(meshes)

def unOverrideNurbs():
    mel.eval('SelectHierarchy')
    
    sel = pm.ls(sl = True)
    
    for s in sel:
        nurbs = ( pm.listRelatives(s, type = 'nurbsCurve'))
        for n in nurbs:
            pm.setAttr('%s.overrideEnabled' % n, False)

# unOverrideNurbs()

def OverrideNurbs():
    mel.eval('SelectHierarchy')
    
    sel = pm.ls(sl = True)
    
    for s in sel:
        nurbs = ( pm.listRelatives(s, type = 'nurbsCurve'))
        for n in nurbs:
            pm.setAttr('%s.overrideEnabled' % n, True)  

# unOverrideNurbs()

def blueOffset():
    mel.eval('SelectHierarchy')
    sel = pm.ls(sl = True)
    for s in sel:
#         try:
#             pm.disconnectAttr('jointLayer.drawInfo', '%s.drawOverride' % s)
#         except Exception as ex:
#             print(ex)
        pm.setAttr( "%s.overrideEnabled" % s, True)
        pm.setAttr('%s.overrideColor' % s, 18)

# blueOffset()



def yellowOffset():
    sel = pm.ls(sl = True)
    for s in sel:
        pm.setAttr( "%s.overrideEnabled" % s, True)
        pm.setAttr('%s.overrideColor' % s, 17)
    
def decoJointLayer():
    mel.eval('SelectHierarchy')
    sel = pm.ls(sl = True)
    for s in sel:
        try:
            pm.disconnectAttr('jointLayer.drawInfo', '%s.drawOverride' % s)
        except Exception as ex:
            print(ex)

# yellowOffset()
# decoJointLayer()

def mirrorButtonIcon():
    sel = pm.ls(sl = True)
    # match name
    if not 'ButtonIcon' in sel[1].name():
        pm.rename(sel[1], sel[0].name().replace('Button', 'ButtonIcon'))
    # connect attributes
    
    try:
        pm.connectAttr('%s.translate' % sel[0],'%s.translate' % sel[1] )
    except Exception as ex:
        print ex
        
    try:
        pm.connectAttr('%s.scaleX' % sel[0],'%s.scaleX' % sel[1] )
    except Exception as ex:
        print ex
        
    try:
        pm.connectAttr('%s.scaleY' % sel[0],'%s.scaleY' % sel[1] )
    except Exception as ex:
        print ex
    
    # duplicate buttonIcon
    # rename copy
    mirrorCopy = pm.duplicate(sel[1], name = sel[1].name().replace('R', 'L') )
    # parent copy in mirrored icon
    pm.parent(mirrorCopy, "MirroredIcons")
    
    # add mirror nodew
    print(mirrorCopy[0].name())
    try:
        pm.connectAttr('%s.translate' % sel[0],'%s.translate' % mirrorCopy[0].name() )
    except Exception as ex:
        print ex
        
    # try:
    #     pm.connectAttr('%s.scaleX' % sel[0],'%s.scaleX' % mirrorCopy[0].name() )
    # except Exception as ex:
    #     print ex
        
    try:
        pm.connectAttr('%s.scaleY' % sel[0],'%s.scaleY' % mirrorCopy[0].name() )
    except Exception as ex:
        print ex
    
    # creation du reverse
#     reverse = pm.shadingNode('reverse', asUtility = True, name = "%sReverse" % sel[1].name())
    reverse = pm.shadingNode('reverse', asUtility = True)
    pm.connectAttr(sel[0].scaleX, reverse.inputX)
    pm.connectAttr(reverse.outputX, mirrorCopy[0].scaleX)
    pm.rename(reverse, "%sReverse" % sel[1].name())


# mirrorButtonIcon()

def connectButtonIcon():
    sel = pm.ls(sl = True)
    # match name
    pm.rename(sel[1], sel[0].name().replace('Button', 'ButtonIcon'))
    if not 'ButtonIcon' in sel[1].name():
        pm.rename(sel[1], sel[0].name().replace('Button', 'ButtonIcon'))
    else:
        pass
    
    # connect attributes
    
    try:
        pm.connectAttr('%s.translate' % sel[0],'%s.translate' % sel[1] )
    except Exception as ex:
        print ex
        
    try:
        pm.connectAttr('%s.scaleX' % sel[0],'%s.scaleX' % sel[1] )
    except Exception as ex:
        print ex
        
    try:
        pm.connectAttr('%s.scaleY' % sel[0],'%s.scaleY' % sel[1] )
    except Exception as ex:
        print ex


 
def unhideIO():
    meshes = pm.ls(sl = True)
    for m in meshes:
        print(m.getShape())
        pm.setAttr('%s.intermediateObject'% m.getShape(), 0)


def renameSelAS():
    sel = pm.ls(sl = True)[0]
    oldText = pm.getAttr(sel.multiObjs)
    newText = oldText.replace('L','RF')
    pm.setAttr(sel.multiObjs, newText)

def createButton():  
    source = "Button_Object"
    sel = pm.ls(sl = True)
    
    startX = 0
    startY = 0
    
    for s in sel:  
        startX += 15
        
        newName = None
        if s.name().startswith('R') and not s.name().startswith('RF') and not s.name().startswith('RB') :
            newName = 'r' + (s.name()[1:])
        elif s.name().startswith('FR'):
            newName = 'fr' + (s.name()[2:])
        elif s.name().startswith('RF'):
            newName = 'rf' + (s.name()[2:])
        elif s.name().startswith('RB'):
            newName = 'rb' + (s.name()[2:])
        else:
            newName = s.name()
    
        copy = pm.duplicate(source, name = "Button_%s" % newName)
        print(copy)
        pm.setAttr((copy[0]).scaleX, 10)
        pm.setAttr((copy[0]).scaleY, 10)
        pm.setAttr((copy[0]).translateX, startX)
        pm.setAttr((copy[0]).translateY, 10)
        pm.setAttr((copy[0]).multiObjs, s.name())

def symetrizeButton():
    root = 'WindowCorner'
    sym = "symetrizer"
    source = pm.ls(sl = True)
    print(source)
    for s in source:
        nameSplit = s.name().split('_')
        
        # rename button
        newName = None
        if nameSplit[1] == 'r':
            nameSplit[1] = 'l'
            gap = '_'
            newName = gap.join(nameSplit)
        elif nameSplit[1] == 'fr':
            nameSplit[1] = 'fl'
            gap = '_'
            newName = gap.join(nameSplit)
        elif nameSplit[1] == 'rf':
            nameSplit[1] = 'lf'
            gap = '_'
            newName = gap.join(nameSplit)
        elif nameSplit[1] == 'rb':
            nameSplit[1] = 'lb'
            gap = '_'
            newName = gap.join(nameSplit)
        
        # duplicate button
        print(newName)
        copy = pm.duplicate(s, name = newName)
        
        # rename multiobjs
        oldSel = pm.getAttr((copy[0]).multiObjs)
        newSel = oldSel.replace('R_', 'L_')
        pm.setAttr((copy[0]).multiObjs, newSel)
        
        # deparent window corner
        # parent symetrizer
        pm.parent(copy[0], sym)
        
        # invert translateX
        oldX = pm.getAttr(copy[0].translateX)
        pm.setAttr(copy[0].translateX, oldX*-1)
        
        # parent windows corner
        pm.parent(copy[0], root)


def hideAllLocalAxis():
    test = pm.ls(dag = True)
    for o in test:
        print(o)
        if o.hasAttr('displayLocalAxis'):
            o.setAttr('displayLocalAxis', 0)

hideAllLocalAxis()

# createButton()
# symetrizeButton()


# correction on IKArm_R
pm.parent('IKArmHandle_R', world = True)
pm.parent('IKFKAlignedArm_R', world = True)
pm.parent('IKmessureConstrainToArm_R', world = True)

ctrTmp = pm.orientConstraint('FKWrist_R', 'IKExtraArm_R')
pm.delete(ctrTmp)

pm.parent('IKArmHandle_R', 'IKArm_R')
pm.parent('IKFKAlignedArm_R', 'IKArm_R')
pm.parent('IKmessureConstrainToArm_R', 'IKArm_R')



