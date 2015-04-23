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


# pm.select(test)