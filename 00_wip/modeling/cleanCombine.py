
import os, sys


import maya.mel as mel

from PySide import QtCore
from PySide import QtGui
import pymel.core as pm


from pprint import pprint

def cleanCombine(sel = pm.ls(sl = True)): 
    bakName = sel[0].nodeName()
    
    res = pm.polyUnite(sel, ch = False)
    
    for s in sel:
        if s:
            pm.delete(s)
    
    if len(res) == 1:
        pm.rename(res, bakName)

cleanCombine()