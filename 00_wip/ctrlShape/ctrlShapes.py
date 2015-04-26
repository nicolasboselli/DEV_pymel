'''
Created on 31 janv. 2015

@author: nico
'''

# execute ctrl mel:(one proc by ctrl? import all proc and call one? insert mel in python function? load mel in dcitionnary? load mel path in dictionnary)
# replace ctrl mel created on Selection

from pprint import pprint
import pymel.core as pm
import maya.mel as mm
import os
from glob import glob





# generate shape dictionnary (name: path)

# def to load procedure
def importCtrl(f):
    '''
    param: f: mel pathfile
    '''
    sourceHandle  = open(f,'r')
    sourceContent = sourceHandle.read()
    sourceHandle.close()
    mm.eval(sourceContent)
    print("import of %s done." % f)


# parse folder, collect mel file and load mel proc
def initShapes():
    search = r'J:\_svn\DEV_pymel\00_wip\ctrls\*.mel'
    shapePath = glob(search)
    for pth in shapePath:
        importCtrl(pth)

# def for create shape from dictionnary with shape name
def createCube():
    oneCube = mm.eval('createCube()')
    pm.select(cl = True)
    return oneCube

# def to replace old shape with new shape
def createNurbsSphere(rad = 2, oneName = "Sphere_Ctrl"):
    circ1 = pm.circle(ch = False, o = True, nr = [1,0,0], r = rad, name = oneName)[0]
    circ2 = pm.circle(ch = False, o = True, nr = [0,1,0], r = rad, name = oneName)[0]
    circ3 = pm.circle(ch = False, o = True, nr = [0,0,1], r = rad, name = oneName)[0]
    pm.parent(circ3.getShape(), circ2.getShape(), circ1, s = True, r = True)
    pm.delete(circ3, circ2)
    return circ1



# pm.select(test)