'''
import sys
sys.path.insert(0, "/USERS/chichang/workspace/ccLookdevToolkit")
import alShaderUtils
reload(alShaderUtils)
alsus = alShaderUtils.AlSurfaceUtil()
alsus.initMatId()
'''

#TODO: check if the shader is assigned to anything.

import mtoa.aovs as aov
import maya.cmds as mc

class AlSurfaceUtil:
    '''
    functions to setup and check alSurface for lookdev
    '''
    def __init__(self):
        #get reference to all alSurface
        print "getting all alSurfaces in scene."
        self.als = mc.ls(type="alSurface")
        #vaaarrr
        self.alIdDict = dict()
        self.NUM_MAT_ID = 8
        self.rgbCount = 1
        self.idCount = 1


    def enableAov(self, aovName):
        #enable aov
        aovi = aov.AOVInterface()
        #a list of enabled aovs
        enabledAovs = mc.ls(type="aiAOV")
        aovNode =  "aiAOV_"+aovName

        if aovNode in enabledAovs:
            print aovName +" already in aov list. set to enable."
            #enable aov
            mc.setAttr(aovNode+".enabled", 1)
        else:
            #set aov to active
            print "adding " + aovName + " to active aovs."
            aovi.addAOV(aovName)



    def initIdColor(self):
        #set all id slots to black

        for s in self.als:
            for id in range(1, self.NUM_MAT_ID+1):
                mc.setAttr(s+".id"+str(id), 0.0, 0.0, 0.0)


    def setupMatId(self, idDict):
        #set material id based on dict

        #set all id to black first
        self.initIdColor()

        print "setting id colors..."
        for shader in idDict.keys():
            print "setting color for => " + shader
            idNumber = idDict[shader]["id"]
            idColor = idDict[shader]["color"]
            if idColor == 1:
                #R
                print  "seting id " + str(idNumber) + " to R ..."
                mc.setAttr(shader+".id"+str(idNumber), 1.0, 0.0, 0.0)
            elif idColor == 2:
                #G
                print  "seting id " + str(idNumber) + " to G ..."
                mc.setAttr(shader+".id"+str(idNumber), 0.0, 1.0, 0.0)
            elif idColor == 3:
                #B
                print  "seting id " + str(idNumber) + " to B ..."
                mc.setAttr(shader+".id"+str(idNumber), 0.0, 0.0, 1.0)


    def initMatId(self):
        #initialize default dict for material id

        #enable the first aov
        self.enableAov("id_"+str(self.idCount))

        for s in self.als:
            
            #each shader as key storesvalue
            self.alIdDict[s] = dict()
            print s
            self.alIdDict[s]["id"] = self.idCount
            self.alIdDict[s]["color"] = self.rgbCount

            print self.alIdDict[s]

            if self.rgbCount == 3:
                #TODO: if id Count greater than NUM_MAT_ID

                self.idCount += 1
                self.enableAov("id_"+str(self.idCount))

                self.rgbCount = 1
            else:
                self.rgbCount += 1

        #just call it for now, orgnize this better later
        self.setupMatId(self.alIdDict)
        #reset
        self.rgbCount = 1
        self.idCount = 1


if __name__ == "__main__":
    #alsu = AlSurfaceUtil()
    #alsu.initMatId()
    pass