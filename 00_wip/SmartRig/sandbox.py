import cleanPipeline.cleanModules as clean
from multiprocessing import Condition
from math import ceil
# reload(clean)
# clean.cleanModules()

from pprint import pprint
import pymel.core as pm
import SmartRig.createHelpers as helpers
import SmartRig.IKFK.SmartRigDef as SRD


test = pm.ls(type = ["multiplyDivide", "plusMinusAverage", "condition"])

for md in test:
    pprint(md)
#     pprint(pm.listConnections(md))