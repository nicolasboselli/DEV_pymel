#-*- coding: utf-8 -*

'''
Created on 11 déc. 2013

@author: nico
'''

"""
maj:
    - conform name shape
    - apply color to all shapes
    - add color name as property
    - create def to scale shape
    
"""

import pymel.core as pm
import maya.mel as mm
import maya.cmds as cmds


def colored(col):
    shapList =[]
    for o in pm.ls(sl= True):
        shapList.append(o.getShape())
        
    for i in range(0,len(shapList)):
        print shapList[i].name()
        shapList[i].overrideEnabled.set(True)
        shapList[i].overrideColor.set(col)

def renameShape():
    refName = pm.ls(sl = True)[0]
    #print (refName.name() + "Shape")
    selToName = refName.getShape()
    #print selToName.name("toto")
    pm.rename(selToName, (refName.name() + "Shape"))
    
# renameShape()
# colored(17)