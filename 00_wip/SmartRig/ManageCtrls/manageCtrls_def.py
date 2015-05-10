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
    cvs = sel.cv
    pm.select(cvs)
    pm.move(move, move, move,moveX = movX, moveY = movY, moveZ = movZ, relative = True,objectSpace = True, worldSpaceDistance  = True )
    pm.select(sel)

# sel = pm.ls(sl = True)
# 
# for s in sel:
#     moveShape(s, movY= True)
# scale cvs
# pm.scale((2, 2, 2),relative = True,objectSpace = True)

# change shape
# change color

    