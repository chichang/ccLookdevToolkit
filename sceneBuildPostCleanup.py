

'''
import sys
sys.path.append("/X/tools/maya/user_python/chichang/")
import sceneBuildPostCleanup
reload(sceneBuildPostCleanup)
spc = sceneBuildPostCleanup.TriPostCleanup()
spc.cleanupShaders()

'''

import maya.cmds as mc
import os

class TriPostCleanup:

    def __init__(self):

        self.debug = 0
        #set ns to root
        mc.namespace(set=":")
        self.allNamespaces = mc.namespaceInfo(lon=True)
        self.cleanTag = "_cleaned"
        self.allSGInUse = []
        self.ignoreList = []
        self.oldNsDict = {}
        self.goodExts = [".exr", ".hdr"]
        self.sceneManagerNode = "sceneManagerScriptNode"

    def cleanupShaders(self):
        '''
        cleanup unused shader versions Triforce left behind when updating lookdevs.
        
        '''
        print "===================="
        print "starting cleanup ..."
        print "===================="

        self.count = 0
        
        allAss = mc.ls(type = "mesh")

        for ass in allAss:
            allOutput = mc.listConnections(ass, d=True)
            for outPut in allOutput:
                outNodeType = mc.nodeType(outPut)
                if outNodeType == "shadingEngine":
                    #if self.debug: print"found SG in use: ", outPut
                    if outPut not in self.allSGInUse:
                        self.allSGInUse.append(outPut)
    
        #list coresbonding lookdev shader namespaces
        for sg in self.allSGInUse:
            if ":" in sg:
                try:
                    #triforce
                    shaderName = sg.split(":")[-1].replace("_shared", "").replace("_vraymeshmtlSG", "")
                    shaderVersion = int(shaderName.split("_")[-1].replace("v", ""))
                    shaderNameList = shaderName.split("_")
                    del shaderNameList[-1]
                    shaderName = ""
                    for i in shaderNameList:
                        shaderName = shaderName+i+"_"
                    shaderName += "v"+str(shaderVersion).zfill(3)

                    if shaderName in self.allNamespaces:
                        self.ignoreList.append(shaderName)

                    else:
                        if self.debug: print "can not find: ", shaderName, "in namespace."
    
                except:
                    #scenebuilder
                    shaderName = sg.split(":")[0]
                    if "lookdev_shaders" in shaderName:
                        self.ignoreList.append(shaderName)

                #else:
                    #if self.debug: print "error parsing: ", sg, " skipping ..."
    
            else:
                if self.debug: print sg, " is root. skipping ..."
    
        print "\nfound lookdev shaders in use:"
        print '\n'.join(self.ignoreList)
        print "\n"

        if self.debug: print "\nchecking version for following sg in use:"
        if self.debug: print '\n'.join(self.allSGInUse) +'\n'

        #start cleanup
        for sg in self.allSGInUse:

            if ":" in sg:
                
                appliedSGNamespace = sg.split(":")[0]

                if appliedSGNamespace in self.allNamespaces:
                    if self.debug: print "lookdev namespace found: ", appliedSGNamespace
                    
                    if self.cleanTag not in appliedSGNamespace:

                        #get namespace version
                        try:
                            version = int(appliedSGNamespace.split("_")[-1].replace("v", ""))
                            if self.debug: print "lookdev version: ", version
                        except:
                            print "could not find version for ", appliedSGNamespace, "... skipping ..."
                            continue

                        assName = appliedSGNamespace.split("_lookdev_shaders")[0]

                        print "searching for unused lookdev for: ", assName, " ..."

                        #multi lookdev?
                        if not assName.isupper():
                            print "Multi lookdev found."
                            cleanAssName = self.cleanUpAss(assName)
                            if cleanAssName in assName:
                                lookdevVarName = assName.replace(cleanAssName, "")
                                assName = cleanAssName
                                print "found lookdev variation name: ", lookdevVarName
                            else:
                                lookdevVarName = None

                            if self.debug: print "asset name: ", assName +"\n"

                            #clean up multilookdev version
                            oldNsDict_var = self.getOldVerNamespace(assName, version, lookdevVarName)
                            oldNsDict = self.getOldVerNamespace(assName, 0)
                            self.cleanLookdevDict(oldNsDict_var)
                            self.cleanLookdevDict(oldNsDict)

                            if self.debug: print oldNsDict_var, self.ignoreList
                            if self.debug: print oldNsDict, self.ignoreList

                        #single lookdev
                        else:
                            oldNsDict = self.getOldVerNamespace(assName, version)
                            if self.debug: print oldNsDict, self.ignoreList
                            self.cleanLookdevDict(oldNsDict)

            else:

                if self.debug: print sg, " is root. skipping ..."

        #done
        self.cleanStats()
        print"\n\n"
        print str(self.count)+" nodes was removed."
        print"\n\n"
        mc.warning("shader cleanup complete, please check script editor for detail.   ~ \(^ .^)/ ~")
    
    def getOldVerNamespace(self, assName, latestVer, variationName = None):
        delDict = {}

        if variationName:
            checkStr = assName+variationName
        else:
            checkStr = assName+"_lookdev_shaders"

        if self.debug: print "searching for: ", checkStr, "in namespace list..."

        #finding namespaces ...
        for ns in self.allNamespaces:

            #pass if it's ignored
            if ns in self.ignoreList:
                #if self.debug: print "shader ", ns, " is in use ... skipping..."
                continue
            
            #only search for lookdev but not shared sg
            if (checkStr in ns) and ("_shared" not in ns):

                if self.cleanTag not in ns:

                    if self.debug:print "found:", ns

                    #look at the version
                    version = int(ns.split("_")[-1].replace("v", ""))
                    if version != latestVer:

                        print "\nfound unused version: ", ns
                        # add to dic for cleanup
                        # add corrisponding shared SG
                        sharedSGNamespace = checkStr+"_shared"+"_v"+str(version)

                        #if cant find return none
                        mc.namespace(set=":")
                        if mc.namespace(exists=sharedSGNamespace):
                            if self.debug: print "found matching shared SG namespace: ", sharedSGNamespace
                            delDict[ns] = sharedSGNamespace

                        else:
                            if self.debug: print "no namespace found: ", sharedSGNamespace
                            delDict[ns] = None

                        self.ignoreList.append(ns)

        return delDict


    def cleanLookdevDict(self, oldNsDict):
        #delete all content in found unused shader namespace
        if oldNsDict and len(oldNsDict)>0:
            print "======================================="
            print "unused versions found for: "#, assName
            print "======================================="
            print "\n".join(oldNsDict)
            print "deleting shader content...\n"
            #deleteContent
            for nsKey in oldNsDict:
                print "deleting ", nsKey, " contents..."
                self.deleteNsContents(nsKey)

                #delete scenebuilder history
                self.cleanSceneBuilderHistory(nsKey)

                #triforce
                if oldNsDict[nsKey]:
                    print "cleaning up shared sg: ", oldNsDict[nsKey]
                    print "deleting ", oldNsDict[nsKey], " contents..."
                    self.deleteNsContents(oldNsDict[nsKey])
                #scenebuilder
                else:
                    print "no shared sg to cleanup for ", nsKey


    def deleteNsContents(self, nameSpace):
        mc.namespace(set=":")
        mc.namespace(set=":"+nameSpace)
        if self.debug: print"current ns: ", mc.namespaceInfo(currentNamespace=True)
        nsContent = mc.namespaceInfo(ls=True, listOnlyDependencyNodes=True)

        if not nsContent:
            return

        for i in mc.namespaceInfo(ls=True, listOnlyDependencyNodes=True):
            
            delStr = i.split(":")[-1]
            
            try:
                print "deleting:", delStr
                #print mc.nodeType(i)
                mc.delete(i)
                self.count += 1

            except:
                if self.debug:print "can not delete: ", i
                pass

        if self.debug: print "renaming namespace: ", nameSpace
        self.setNsCleaned(nameSpace)

    def setNsCleaned(self, oldName):
            mc.namespace(set=":")
            for i in range(0, 9999):
                newName = self.cleanTag+str(i)
                if mc.namespace(exists=newName):
                    continue
                else:
                    break
            #newName = oldName.replace("_lookdev_shaders", "")+self.cleanTag
            try:
                mc.namespace(rm=oldName)
                #mc.namespace(ren = (oldName, newName))
                if self.debug: print  "deleting namespace: ", newName
            except:
                mc.namespace(ren = (oldName, newName))
                if self.debug: print "error renaming namespace: ", oldName

    def cleanUpAss(self, assName):
        newAss = ""
        ls = assName.split("_")
        for i in ls:
            if i.isupper():
                newAss += i+"_"
        return newAss[:-1]

    def sceneManagerScriptAttr(self):
        for i in mc.listAttr("sceneManagerScriptNode"):
            print i

    def cleanStats(self):
        dirs = []
        dirtyFiles=[]
        lambertOnes=[]
        noneMipmapFiles=[]

        fileList = mc.ls(type = "file")
        for f in fileList:
            fPath = mc.getAttr(f+".fileTextureName")
            fileExt = os.path.splitext(fPath)[-1]
            if fileExt not in self.goodExts:
                dirtyFiles.append(fPath)

            fFilter = mc.getAttr(f+".filterType")
            if fFilter != 1:
                noneMipmapFiles.append(fPath)

        if len(dirtyFiles)>0:
            print "==================================="
            print " bad textures still found in scene."
            print "==================================="
            for p in dirtyFiles:
                print p

        #if len(noneMipmapFiles)>0:
        #    print "==================================="
        #    print " none mipmap texture filter found."
        #    print "==================================="
        #    for f in noneMipmapFiles:
        #        print f

        #lambert 1 check
        sg = "initialShadingGroup"
        allOutput = mc.listConnections(sg, s=True, sh=True)
        for o in allOutput:
            nodeType = mc.nodeType(o)
            if nodeType == "mesh":
                lambertOnes.append(o)

        if len(lambertOnes)>0:
            print "========================================"
            print " following meshs have Lambert 1 applied."    
            print "========================================"
            for m in lambertOnes:
                print m

    def cleanSceneBuilderHistory(self, asset):
        attr = self.sceneManagerNode+"."+asset
        try:
            mc.deleteAttr(attr)
            if self.debug: print "deleting scenebuilder script node attr: ", attr
            return attr
        except:
            if self.debug: print "delete attribute fail: ", attr
            return None
