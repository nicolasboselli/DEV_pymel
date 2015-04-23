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

# find position
for s in sel:
    if s.hasAttr('qaFkPaCstPoints'):
        vertList = s.getAttr('qaFkPaCstPoints')
        vertParent  = vertList.split(' ')
    #     pprint(test)
        xTotal = 0
        yTotal = 0
        zTotal = 0
        
        for vp in vertParent:
            vert = pm.MeshVertex(vp)
            xTotal += (vert.getPosition())[0]
            yTotal += (vert.getPosition())[1]
            zTotal += (vert.getPosition())[2]
            
        newPos = [xTotal/len(vertParent), yTotal/len(vertParent), zTotal/len(vertParent) ]
        
        
        # find selection Parent grp
        parent = s.getParent()
        print(parent)
        
        # create test
        locTest = pm.spaceLocator(name = 'locTest')
        locTest.translate.set(newPos)
        root = parent.getParent()
        locTest.setParent(root)
        goodPos = (locTest.translate.get())
        pm.delete(locTest)
        
        # set group position 
        parent.translate.set(goodPos)
    else:
        'no attribute'
    

#
 
