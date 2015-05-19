'''
Created on 6 mai 2015

@author: nicolas_2
'''

from pprint import pprint
import pymel.core as pm
import SmartRig.createHelpers as helpers
import SmartRig.IKFK.SmartRigDef as SRD
import maya.mel as mm
import maya.OpenMaya as om


def moveShape(sel, movX = False, movY = False, movZ = False, move = 2):
    pm.select(clear = True)
    shapList = (pm.listRelatives(sel, shapes = True))
    for s in shapList:
        cvs = s.cv
        pm.select(cvs, add = True)
    
    pm.move(move, move, move,moveX = movX, moveY = movY, moveZ = movZ, relative = True,objectSpace = True, worldSpaceDistance  = True )
    pm.select(sel)

# 
# for s in sel:
#     moveShape(s, movY= True)
# scale cvs
# pm.scale((2, 2, 2),relative = True,objectSpace = True)

def scaleShape(sel, scalX = False, scalY = False, scalZ = False, scale = 2):
    pm.select(clear = True)
    shapList = (pm.listRelatives(sel, shapes = True))
    for s in shapList:
        cvs = s.cv
        pm.select(cvs, add = True)
        
    pm.scale(scale, scale, scale, scaleX = scalX, scaleY = scalY, scaleZ = scalZ, relative = True,objectSpace = True)
    pm.select(sel)

# sel = pm.ls(sl = True)
# for s in sel:  
#     moveShape(s, movX = True)
#     cvs = s.cv
#     print cvs
#     pm.select(cvs)
    
# change shape
# change color

    