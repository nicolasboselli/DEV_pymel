'''
Created on 23 avr. 2015

@author: nicolas_2
'''
from pprint import pprint
import pymel.core as pm

def initMotionSystem ():
    motionGrpTmp = None
    motion_system_exists = False
    motionGrpAr = pm.ls('motion_system')
    if len(motionGrpAr) > 0 : motion_system_exists = True
    if not motion_system_exists : motionGrpTmp = pm.group(em = True, name = 'motion_system')
    else: motionGrpTmp = motionGrpAr[0]
    return motionGrpTmp

def initDeformSystem ():
    defGrpTmp = None
    deformation_system_exists = False
    defGrpAr = pm.ls('deformation_system')
    if len(defGrpAr) > 0 : deformation_system_exists = True 
    if not deformation_system_exists : defGrpTmp = pm.group(em = True, name = 'deformation_system')
    else: defGrpTmp = defGrpAr[0]
    return defGrpTmp