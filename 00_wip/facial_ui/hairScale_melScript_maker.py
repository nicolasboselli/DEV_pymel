'''
Created on 3 dec. 2014

@author: gamma project
'''

import os, sys

import maya.mel as mel

from PySide import QtCore
from PySide import QtGui
import pymel.core as pm

from pprint import pprint

import re

# create mel
breakHierarchyMelGuide = r'C:\vic_movie_misc\scriptGuides\breakHierarchyMelGuide.mel'
rebuidHierarchyMelGuide = r'C:\vic_movie_misc\scriptGuides\rebuidHierarchyMelGuide.mel'


breakLines = []
rebLines = []

# find strand group
relat = pm.listRelatives('hair_joint_grp', children = True, type = 'transform')
for grp in relat:
    joints = pm.listRelatives(grp, children = True, type = 'joint')
    comment = "\n\n// %s breaking hierarchy" % grp.name()
    breakLines.append(comment)
    
    rebCom = "\n\n// %s rebuild hierarchy" % grp.name()
    rebLines.append(rebCom)
    
    for j in joints:
        goodJoints =  []
        rebJoints = []
        if not j.name().startswith('T_'):
            jointsTmp = pm.listRelatives(j, allDescendents = True, type = 'joint')
            goodJoints.append(j)
            
            for elt in jointsTmp:
                goodJoints.append(elt)
                rebJoints.append(elt)
                
            rebJoints.append(j)
            # write break mel guide
            for j in goodJoints:
                command = ('\ncatch(`parent %s %s`);' % (j.name(), grp.name()))
                breakLines.append(command)

            # write rebuild mel guide
            for i,o in enumerate(rebJoints):
                if i+1<len(rebJoints):
                    rebCmd = ('\ncatch(`parent %s %s`);' % (o.name(), rebJoints[i + 1].name()))
                    rebLines.append(rebCmd)
                


breakFile = open(breakHierarchyMelGuide, 'w+')
breakFile.writelines(breakLines)
breakFile.close()

rebFile = open(rebuidHierarchyMelGuide, 'w+')
rebFile.writelines(rebLines)
rebFile.close()

