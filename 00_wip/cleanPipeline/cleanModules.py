'''
Created on 29 dec. 2014

@author: nicolas_2
'''
import sys

from pprint import pprint
from mhlib import PATH


# clean python PATH

# add wip python path
wipPath = r"J:\github\DEV_pymel\00_wip"
# wipPath = r"J:\_svn\DEV_pymel\00_wip"
sys.path.append(wipPath)
pprint(sys.path)


def cleanModules():
# clean python modules
    l = [
    'SmartRig',
    'IKFK',
    'MyMayaScripts',
    'ctrlShape'
    ]
    
    
    print("#\n#\n# Deletion of following modules from sys.\n#")
    pprint(l)
    #print("#")
    count=0
    delCount=0
    for item in sorted(sys.modules.keys()):
        print(item)
        isDel = False
        for x in l:
            if x in item:
                count+=1
                try:
                    del(sys.modules[item])
                    isDel = True
                    #print ("# deleted '%s'" %(item))
                    delCount+=1
                except:
                    print "# ! Can't delete {0}".format(item)
                    pass
        if not isDel:
            #print item
            pass
    print("#\n# ... Deleted %d/%d modules" %(delCount,count))

