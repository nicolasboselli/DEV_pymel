'''
Created on 5 dec. 2014

@author: gamma project
'''
import os, sys

import maya.mel as mel

from PySide import QtCore
from PySide import QtGui
import pymel.core as pm

from pprint import pprint

sel = pm.ls(sl = True)

world = pm.PyNode('world')
worldInverse = pm.PyNode('world_inverse')

for s in sel:
    parent = s.getParent()
    print(s.name())
    if 'R_' in s.name():
        sym = pm.ls(s.name().replace('R_', 'L_'))[0]
        symParent = sym.getParent()
        print(sym.name())
        print(symParent.name())
        
        
        # backup parents
        oldParent = parent.getParent()
        print(oldParent)
        oldSymParent = symParent.getParent()
        print(oldSymParent)
        
        # parent to world and world_inverse
        pm.parent(parent, world)
        print(world)
        pm.parent(symParent, worldInverse)
        print(worldInverse)
        
        # translate
        symParent.rotate.set(parent.rotate.get())
        symParent.translate.set(parent.translate.get())
        
        # reparent to old parent
        pm.parent(parent, oldParent)
        pm.parent(symParent, oldSymParent)
        
        

