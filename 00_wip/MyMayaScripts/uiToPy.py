import pysideuic
import os

if __name__ == '__main__':
    path = os.path.dirname(__file__)
    print(path)
    pysideuic.compileUiDir(os.path.join(path))


    print "done"