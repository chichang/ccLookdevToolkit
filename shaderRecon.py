
##maya Tool collect

import os
import maya.cmds as mc
import shutil

def removeAllCache():
    '''
    remove all dynamic caches in the scene
    '''
    caches = mc.ls(type = "cacheFile")
    print caches
    
    for i in caches:
        mc.delete(i)

#sgrp = mc.ls(sl=True)[0]
#print mc.nodeType(sgrp)

sgrpList = mc.ls(type="shadingEngine")
print sgrpList

for sg in sgrpList:
    print sg
    sg_connections = mc.listConnections(sg)
    
    for con in sg_connections:
        #print mc.nodeType(con)
        shapes = cmds.listRelatives(con)
        print shapes
        if mc.nodeType(con) == "mesh":
            pass

import maya.cmds as mc
def texStatus():
    '''
    quick check stats for all the texture files in the scene.
    '''
    dirs = []
    fileList = mc.ls(type = "file")
    print "Found", str(len(fileList)), "files in the scene."
    for f in fileList:
        fPath = mc.getAttr(f+".fileTextureName")
        dirPath = os.path.split(fPath)[0]
        print f + ":"
        print fPath
        if dirPath not in dirs:
            dirs.append(dirPath)
    print "========= All File Path ==============="
    for p in dirs:
        print p
    print "========= File Path not Exist ==============="
    for p in dirs:
        try:
            if not os.path.exists(p):
                print p
        except e:
            print error

    print "========= File Path Empty ==============="
    
    for p in dirs:
        try:
            if len(os.listdir(p)) == 0:
                print p
        except:
            pass

    print "========= src texture missing ==============="

    for p in dirs:

        src_dirPath = os.path.split(p)[0]
        src_dirVersion = os.path.split(p)[1]

        if "tinyres" in src_dirPath:
            src_dirPath = src_dirPath.replace("tinyres", "src")
        
        elif "lores" in src_dirPath:
            src_dirPath = src_dirPath.replace("tinyres", "src")

        elif "midres" in src_dirPath:
            src_dirPath = src_dirPath.replace("midres", "src")

        elif "fullres" in src_dirPath:
            src_dirPath = src_dirPath.replace("fullres", "src")

        elif "hires" in src_dirPath:
            src_dirPath = src_dirPath.replace("hires", "src")
        
        
        #get latest srcversion from shotgun
        #latestSrcVer = shotgun.getLastVersion(os.getenv("SHOW"), os.getenv("SHOT"), os.path.split(src_dirPath)[1])
        latestSrcVer = os.path.join(src_dirPath, src_dirVersion)
        try:
            if not os.path.exists(latestSrcVer):
                print latestSrcVer
        except:
            pass
 

def grabSrcTex(copy_src_dir):
    '''
    copy all the "src" version of texture to input directory.
    '''
    dirs = []

    missing_dirs = []

    udimTag = "<UDIM>"
    resList = ["tinyres","lores","midres","hires","fullres"]
    
    #copy_src_dir = "/X/projects/vulcan/SHOTS/FORUM/chichang/textures/OA_STREET_A/v001"
    
    fileList = mc.ls(type = "file")
    
    print "Found", str(len(fileList)), "files in the scene."
    
    for f in fileList:
        #print path
        fPath = mc.getAttr(f+".fileTextureName")
        #print dir
        dirPath = os.path.split(fPath)[0]
        fileName = os.path.split(fPath)[1]

        src_dirPath = os.path.split(dirPath)[0]
        src_dirVersion = os.path.split(dirPath)[1]

        if "tinyres" in src_dirPath:
            src_dirPath = src_dirPath.replace("tinyres", "src")
        
        elif "lores" in src_dirPath:
            src_dirPath = src_dirPath.replace("tinyres", "src")

        elif "midres" in src_dirPath:
            src_dirPath = src_dirPath.replace("midres", "src")

        elif "fullres" in src_dirPath:
            src_dirPath = src_dirPath.replace("fullres", "src")

        elif "hires" in src_dirPath:
            src_dirPath = src_dirPath.replace("hires", "src")

        else:
            print "!!!!!!!!!cant process: ", src_dirPath

        #print src_dirPath

        if not os.path.exists(src_dirPath):
            if src_dirPath not in missing_dirs:
                missing_dirs.append(src_dirPath)
                print "!!!!!!!!!!  SRC Texture Path Missing: ", src_dirPath
            continue

        full_src_dir = os.path.join(src_dirPath,src_dirVersion)

        if not os.path.exists(full_src_dir):

            if full_src_dir not in missing_dirs:
                missing_dirs.append(full_src_dir)
                #print "!!!!!!!!!!  SRC Texture Path Missing: ", full_src_dir
            continue

        #listDir
        all_files_in_dir = os.listdir(full_src_dir)

        if len(all_files_in_dir) == 0:
            print "DIR EEEMMMMPPPPTTTYYY!!! ", full_src_dir

        fileName_no_ext = os.path.splitext(fileName)[0]
        fileName_no_ext = fileName_no_ext.replace(udimTag,"")

        for f in all_files_in_dir:
            if fileName_no_ext in f:

                #file to get
                full_file_path = os.path.join(full_src_dir,f)

                #path to copy to 
                copy_file_path = os.path.join(copy_src_dir,f)

                #doublecheck ....
                if not os.path.exists(full_file_path):
                    print full_file_path

                if not os.path.exists(copy_file_path):
                    try:
                        shutil.copy2(full_file_path, copy_src_dir)
                    except:
                        print "cant copy image: ", full_file_path
    for d in missing_dirs:
        print "!!!!!!!!!!  SRC Texture Path Missing: ", d



def reconPath():

    dirs = []

    missing_dirs = []

    udimTag = "<UDIM>"
    resList = ["tinyres","midres","hires","fullres"]
    copy_src_dir = "/X/projects/vulcan/SHOTS/BA_STREET/chichang/textures/BA_STREET_REAR/v001"
    
    fileList = mc.ls(type = "file")

    print "Found", str(len(fileList)), "files in the scene."
    
    for f in fileList:
        #print path
        fPath = mc.getAttr(f+".fileTextureName")
        #print dir
        dirPath = os.path.split(fPath)[0]
        fileName = os.path.split(fPath)[1]

        src_dirPath = os.path.split(dirPath)[0]
        src_dirVersion = os.path.split(dirPath)[1]

        fileName_no_ext = os.path.splitext(fileName)[0]
        fileName_ext = os.path.splitext(fileName)[1]
        
        if fileName_ext == ".exr":
            continue
        
        newName = fileName_no_ext + ".exr"
        
        newPath = os.path.join(copy_src_dir, newName)

        mc.setAttr(f+".fileTextureName", newPath)
        print newPath



def replaceAllFilePath(newTexDir, newExt):

    fileList = mc.ls(type = "file")
    
    print "Found", str(len(fileList)), "files in the scene."
    
    for f in fileList:
        #print path
        fPath = mc.getAttr(f+".fileTextureName")
        #print dir
        if os.getenv("SHOT") in fPath:
        
            dirPath = os.path.split(fPath)[0]
            fileName = os.path.split(fPath)[1]
    
            src_dirPath = os.path.split(dirPath)[0]
            src_dirVersion = os.path.split(dirPath)[1]
    
    
            fileName_no_ext = os.path.splitext(fileName)[0]
            fileName_ext = os.path.splitext(fileName)[1]
            
            newName = fileName_no_ext + newExt
            
            newPath = os.path.join(newTexDir, newName)
            
            print "changing ", fPath, "to:\n", newPath
            mc.setAttr(f+".fileTextureName", newPath, type="string")


#replaceAllFilePath("/X/projects/vulcan/SHOTS/CORVUS/lib/textures/CORVUS/CORVUS_tex_src/v001", ".tif")


def replacePath():

    dirs = []

    missing_dirs = []

    udimTag = "<UDIM>"
    resList = ["tinyres","midres","hires","fullres"]
    copy_src_dir = "/X/projects/vulcan/SHOTS/BA_STREET/chichang/textures/BA_STREET_REAR/v001"
    
    fileList = mc.ls(type = "file")
    
    print "Found", str(len(fileList)), "files in the scene."
    
    for f in fileList:
        #print path
        fPath = mc.getAttr(f+".fileTextureName")
        #print dir
        dirPath = os.path.split(fPath)[0]
        fileName = os.path.split(fPath)[1]

        src_dirPath = os.path.split(dirPath)[0]
        src_dirVersion = os.path.split(dirPath)[1]


        fileName_no_ext = os.path.splitext(fileName)[0]
        fileName_ext = os.path.splitext(fileName)[1]
        
        if fileName_ext == ".exr":
            continue
        
        newName = fileName_no_ext + ".exr"
        
        newPath = os.path.join(copy_src_dir, newName)
        print newPath

        mc.setAttr(f+".fileTextureName", newPath, type="string")




#match all shader by geo name
def matchShaderByName(q=False, ignoreIndex = False):

    mc.setAttr("lambert1.color", 0.271, 0.5, 0.5)

    from textureExport import xgUtils
    su = xgUtils.ccSysUtil()
    #srcTag = "city_block_eb"m
    #targetTag = "block_ef"

    root_grp = mc.ls(sl=True)

    if len(root_grp) < 2:
        mc.warning("please select source and target.")
        return

    source = root_grp[0]
    target = root_grp[1]

    print "source: ", source
    print "target: ", target

    #get all mesh shapes
    all_source_shape = mc.listRelatives(source, ad=True, type = "mesh")
    all_target_shape = mc.listRelatives(target, ad=True, type = "mesh")

    source_found = []

    for source_shape in all_source_shape:
        clean_source_name = source_shape.split(":")[-1]

        #if srcTag in clean_source_name:
            #clean_source_name = clean_source_name.replace(srcTag, targetTag)

        if ignoreIndex:
            clean_source_name = removeNameIndexes(clean_source_name)

        #find if shape matches
        for target_shape in all_target_shape:
            
            clean_target_name = target_shape.split(":")[-1]
            
            if ignoreIndex:
                clean_target_name = removeNameIndexes(clean_target_name)
                print clean_target_name

            if clean_source_name == clean_target_name:
                
                #match shader.
                matSGName = mc.listConnections(source_shape, type = "shadingEngine")
                print "matching shape: ", source_shape, " shader ", matSGName[0], " to ", target_shape

                mc.sets(target_shape,e = 1, forceElement = matSGName[0])
                source_found.append(target_shape)

    if not q:
        print "match shader done."
        print "=============== Fail to match shaders on ==============="
        fail_list =  su.listDiff(source_found,all_target_shape)
        for i in fail_list:
            print i



def removeNameIndexes(string1):
    index = map(int, re.findall(r'\d+', string1))
    if len(index) != 0:
        string1 = string1.replace(str(index[-1]), "")
        return string1
    else:
        return string1


def setAllGamma(val):
    allGamma = mc.ls(type = "gammaCorrect")
    for i in allGamma:
        print "setting", i ,"gamma value to: ", val
        mc.setAttr(i+".gamma", val,val,val)

def setAllFileFilter():
    allFile = mc.ls(type = "file")
    for i in allFile:
        print "setting", i ,"filter type to : ", "Mipmap"
        mc.setAttr(i+".filterType", 1)

def setAllVMeshOffset(val):
    vrayMeshList = mc.ls(type = "VRayMesh")
    for m in vrayMeshList:
        mc.setAttr(m+".animOffset", val)


vrayMtls = mc.ls(type = "VRayMtl")
for m in vrayMtls:
    rflSub = mc.getAttr(m+".reflectionSubdivs")
    rfraSub = mc.getAttr(m+".refractionSubdivs")
    print m + ": " + str(rflSub)
    print m + ": " + str(rfraSub)
    rflSub = mc.setAttr(m+".reflectionSubdivs", 8)
    rfraSub = mc.setAttr(m+".refractionSubdivs", 8)
##set all file filter type

import shotgun
print shotgun.getLastVersion("strain", "MASTER", "MASTER_NOSE_lookdev")
print shotgun.getLastVersion("strain", "MASTER", "MASTER_NOSE_tex_src")
print shotgun.getLastVersion("strain", "MASTER", "MASTER_NOSE_tex_fullres")


for a in nuke.allNodes():
    if 'Read' in a['name'].value():
        print a['file'].value()


import maya.cmds as mc
mesh = "GR226_ROSEMARY_0_lte:rosemary_body_cn_geoShape"

mc.connectAttr(mesh+".outMesh", "geoConnector1.localGeometry")
mc.connectAttr(mesh+".worldMatrix[0]", "geoConnector1.worldMatrix")
mc.connectAttr(mesh+".message", "geoConnector1.owner")




##TEX INFO

def oiioTextureInfo():
    
    #imports
    import maya.cmds as mc
    import subprocess
    import os
    
    udimTags = ["<udim>", "<UDIM>"]
    
    #subprocess call
    callList = ["oiiotool", "--info", "-v"]
    
    #get selected file node
    try:
        fileNode = mc.ls(sl=True, type="file")[0]
        print "getting path for: " + fileNode
    except:
        mc.warning("select a file node please.")
        return

    filePath = mc.getAttr(fileNode+".fileTextureName")
    print filePath

    for tag in udimTags:
        
        if tag in filePath:
            #find one of the textures
            for i in range (1001, 1099):
                checkPath = filePath.replace(tag, str(i))
                print checkPath
                
                if os.path.exists(checkPath):
                    print "found texture: " + checkPath
                    filePath = checkPath
                    break
        else:
            pass

    if os.path.exists(filePath):
        #get info
        print "getting texture info..."
        
        callList.append(filePath)
        print "calling: ", callList
        try:
            p = subprocess.Popen(callList, stdout=subprocess.PIPE)
            out, err = p.communicate()
            
            message = "====================================================\n"
            message += "Texture info for : " + fileNode + "\n"
            message += "Texture checked: " + filePath + "\n"
            message += "====================================================\n\n"
            message += out
            
        except:
            message = "Error calling oiiotool."

        #display result
        #mc.confirmDialog( title='Confirm', message='Are you sure?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        mc.confirmDialog( title='Texture Info: ' + fileNode, message=message, button=['OK'], defaultButton='OK')

        return

        
    else:
        mc.warning("could not find any texture. does texture exist ?")
        return





import maya.cmds as mc
def deleteMAttrs():
    attrsToDelete = [ "mShape", "mSubd", "mMaterial" ]
    #delete on all meshes
    allMesh = mc.ls(type="mesh")
    for mesh in allMesh:
        attrs = mc.listAttr(mesh)
        for attr in attrsToDelete:
            if attr in attrs:
                toDelete = mesh+"."+attr 
                #check for locked attr
                if mc.getAttr(toDelete, l=True):
                    mc.setAttr(toDelete, l=False)
                #delete attr
                print "deleting:  ", toDelete
                mc.deleteAttr(toDelete)


import maya.cmds as mc
def rmNamespace():
    allNodes = mc.ls()
    for i in allNodes:
        if "vray_lookdev_lgt_rig_v002" in i:
            print i
            newName = i.replace("vray_lookdev_lgt_rig_v002:","")
            print newName
            try:
                mc.rename(i,newName)
            except:
                pass
        else:
            pass

rmNamespace()



#match all shader by geo name
def matchShaderByPosition(q=False, errorThres = 1):
    
    defaultSeed = 1
    #mc.setAttr("lambert1.color", 0.271, 0.5, 0.5)

    import math
    from textureExport import xgUtils
    su = xgUtils.ccSysUtil()

    root_grp = mc.ls(sl=True)

    if len(root_grp) < 2:
        mc.warning("please select source and target.")
        return

    source = root_grp[0]
    target = root_grp[1]

    print "source: ", source
    print "target: ", target

    #get all mesh shapes
    all_source_shape = mc.listRelatives(source, ad=True, type = "mesh")
    all_target_shape = mc.listRelatives(target, ad=True, type = "mesh")

    source_found = []

    for source_shape in all_source_shape:
        
        #handle name spaces better here.....
        clean_source_name = source_shape.split(":")[-1]
        
        #get source shape vert count
        source_vNum = mc.polyEvaluate(source_shape, v=True)

        #find if shape matches
        for target_shape in all_target_shape:
            
            clean_target_name = target_shape.split(":")[-1]

            target_vNum = mc.polyEvaluate(target_shape, v=True)

            #if same amount
            if source_vNum == target_vNum:

                #find vert
                #mc.xform("COMMUNITY_mdl_0:extenstion_1_concrete_7_cn_geoShape.vtx[1]", t=True, ws=True, q=True)
                source_vPos = mc.xform(source_shape+".vtx[" + str(defaultSeed) + "]", t=True, ws=True, q=True)
                print source_vPos
                target_vPos = mc.xform(target_shape+".vtx[" + str(defaultSeed) + "]", t=True, ws=True, q=True)
                print target_vPos
                
                #print source_vPos - target_vPos
                #-50 < (source_vPos[0]-source_vPos[0]) < 50
                
                errorCheck = (source_vPos[0]-target_vPos[0]) + (source_vPos[1]-target_vPos[1]) + (source_vPos[2]-target_vPos[2])
                print errorCheck
                
                #if pass match check
                if math.fabs(errorCheck) < errorThres:
                    #print "Match!!!"
                    #match shader.
                    matSGName = mc.listConnections(source_shape, type = "shadingEngine")
                    print "matching shape: ", source_shape, " shader ", matSGName[0], " to ", target_shape
                    mc.sets(target_shape,e = 1, forceElement = matSGName[0])
                    
                    all_target_shape.remove(target_shape)


    if not q:
        print "match shader done."
        print "=============== Fail to match shaders on ==============="
        for i in all_target_shape:
            print i


'''

BA_LADDER_ANIM_mdl maya_mdl one mb maya/scenes/model "Anim rez maya mdl for animation and export"                                      
BA_LADDER_ANIM_mdl_TD maya_mdl_TD one ma maya/scenes/model/TD "Anim rez maya mdl in ascii format for rigging"                          
BA_LADDER_ANIM_mdl_techcheck maya_mdl_TC one ma maya/scenes/model/WRK "maya mdl in ascii format for technical approval"                
BA_LADDER_art_dept_ref dmp dmp dir reference "Directory of ref from art dept"                                                          
BA_LADDER_cyberscan image dir dir reference "Directory of scan geo"                                                                    
BA_LADDER_export maya_export one mb maya/scenes/rig "maya rig for abc export"                                                          
BA_LADDER_export_TD maya_export_TD one ma maya/scenes/rig/TD "maya rig for abc export"                                                 
BA_LADDER_lookdev maya_ldv one ma maya/scenes/lighting "maya look development file"                                                    
BA_LADDER_lookdev_dir dmp dmp dir images/ltm "Look development images directory"                                                       
BA_LADDER_lookdev_ref dmp dmp dir images/ltm "Look development reference images directory"                                             
BA_LADDER_lookdev_techcheck maya_ldv_TC one ma maya/scenes/lighting/WRK "maya look development file for technical approval"            
BA_LADDER_lookdev_tt seq seq dir images/ltm "Look development turn table"                                                              
BA_LADDER_mdl maya_mdl one mb maya/scenes/model "maya mdl for animation and export"                                                    
BA_LADDER_mdl_TD maya_mdl_TD one ma maya/scenes/model/TD "maya mdl in ascii format for rigging"                                        
BA_LADDER_mdl_techcheck maya_mdl_TC one ma maya/scenes/model/WRK "maya mdl in ascii format for technical approval"                     
BA_LADDER_modeldev_dir dmp dmp dir images/ltm "Model development images directory"                                                     
BA_LADDER_modeldev_ref dmp dmp dir images/ltm "Model development reference images directory"                                           
BA_LADDER_modeldev_tt seq seq dir images/ltm "Model development turn table"                                                            
BA_LADDER_photo_survey dmp dmp dir reference "Directory of images"                                                                     
BA_LADDER_rig maya_rig one mb maya/scenes/rig "maya rig for animation"                                                                 
BA_LADDER_rig_TD maya_rig_TD one ma maya/scenes/rig/TD "maya rig for animation"                                                        
BA_LADDER_tex_dir texture_dir dir dir textures "textures for the Digitial Asset"                                                       
BA_LADDER_texturedev_dir dmp dmp dir images/ltm "Texture development images directory"                                                 
BA_LADDER_texturedev_ref dmp dmp dir images/ltm "Texture development reference images directory"                                       
BA_LADDER_texturedev_tt seq seq dir images/ltm "Texture development turn table"                                                        
BA_LADDER_vendor_ref dmp dmp dir reference "Directory of ref from vendor"  

                result[col_name].append({'name':asset.name(), 
                                         'type':asset.type(),
                                         'dirFlag':asset._myDirFlag,
                                         'extension':asset.extension(),
                                         'publishDir':asset.publishDir(),
                                         'description':asset.description(),
                                         'category':asset.category(),
                                         'type':asset.type(),
                                         })

'''

#match all shader by geo name


reconFile = '/USERS/chichang/Documents/shaderReconTemp.json'

def writeShaderRecon(q=False, ignoreIndex = False):
    mc.setAttr("lambert1.color", 0.271, 0.5, 0.5)
    import json
    from textureExport import xgUtils
    su = xgUtils.ccSysUtil()

    #srcTag = "city_block_eb"m
    #targetTag = "block_ef"

    root_grp = mc.ls(sl=True)

    if len(root_grp) < 1:
        mc.warning("please select source.")
        return

    source = root_grp[0]
    #target = root_grp[1]

    print "source: ", source
    #print "target: ", target

    #get all mesh shapes
    all_source_shape = mc.listRelatives(source, ad=True, type = "mesh")
    print all_source_shape
    #all_target_shape = mc.listRelatives(target, ad=True, type = "mesh")
    #print all_target_shape
    source_found = []
    shaderReconDict = {}

    #looping through src shape and look for target to match
    for source_shape in all_source_shape:
        clean_source_name = source_shape.split(":")[-1]
        #print clean_source_name
        #if srcTag in clean_source_name:
            #clean_source_name = clean_source_name.replace(srcTag, targetTag)

        if ignoreIndex:
            clean_source_name = removeNameIndexes(clean_source_name)

        srcSGName = mc.listConnections(source_shape, type = "shadingEngine")[0]
        
        #item = self.item(index)
        #name = item.text()
        #path = item.data(32)
        shaderReconDict[source_shape]=srcSGName

    data = shaderReconDict
    with open(reconFile, 'w') as outfile:
        json.dump(data, outfile)



reconFile = '/USERS/chichang/Documents/shaderReconTemp.json'
ns = ""
def shaderRecon():
    import json
    #from textureExport import xgUtils
    #su = xgUtils.ccSysUtil()
    root_grp = mc.ls(sl=True)
    
    if len(root_grp) < 1:
        mc.warning("please select target.")
        return

    target = root_grp[0]
    print "target: ", target

    #get all mesh shapes
    all_target_shape = mc.listRelatives(target, ad=True, type = "mesh")
    print all_target_shape

    source_found = []
    shaderReconDict = {}

    #json
    try:
        json_data = open(reconFile)
        data = json.load(json_data)
    except:
        print "error"
        pass

    for name, path in data.iteritems():
        
        print name, path

        #namespaces
        path = ns+":"+path
        try:
            mc.sets(name,e = 1, forceElement = path)
            print "matching shape: ", name, " shader ", path
        except:
            print "error connecting shader to :"+name

        #assing shader
        #self.addBookmark(path, name)


        '''
        #find if shape matches
        for target_shape in all_target_shape:
            
            clean_target_name = target_shape.split(":")[-1]
            print clean_target_name
            if ignoreIndex:
                clean_target_name = removeNameIndexes(clean_target_name)
                #print clean_target_name

            if clean_source_name == clean_target_name:
                
                #match shader.
                matSGName = mc.listConnections(source_shape, type = "shadingEngine")
                print "matching shape: ", source_shape, " shader ", matSGName[0], " to ", target_shape

                mc.sets(target_shape,e = 1, forceElement = matSGName[0])
                source_found.append(target_shape)
        '''





#http://pymotw.com/2/imp/

#import imp
#foo = imp.find_module('/X/tools/binlinux/apps/Mari2.6v4/3rdParty/lib/python2.6/site-packages/PySide/')
#foo = imp.find_module('PySide')
#print foo
#['/X/tools/binlinux/apps/Mari2.6v1/3rdParty/lib/python2.6/site-packages/PySide']
#['/X/tools/python/3rd_party/linux_python2.7/PySide']

#/USERS/chichang/lib64:/X/projects/fom/SHOTS/TRAILER_C/chichang/lib64:/X/projects/fom/SHOTS/TRAILER_C/lib/lib64:/X/projects/fom/lib64:/X/tools/liblinux:/X/tools/binlinux/arnold/arnold-4.2.1.2/bin:/X/tools/binlinux/apps/peregrine/yeti-UNK/maya2014/bin:/X/tools/python/bin/linux_python2.7/lib:/X/tools/binlinux/vray/maya2015/vray_2.45.01.24958/maya/lib:/X/tools/binlinux/apps/RisingSunResearch/cineSpace:/X/tools/binlinux/sesi/hfs13.0.547/dsolib:/X/tools/binlinux/apps/OFX/Plugins/genarts/SapphireOFX/lib64:/X/tools/XRender/lib:/usr/lib64:/usr/lib:/lib:.
#tmi
# IN130 door lock texture / rig
# CB030 city of bones texture.
# IN210 institute bridge texture/lookdev
# GH005 institue greenhouse texture/lookdev
# GH020 FX, butterfly animation
# GH030 FX, butterfly animation
# GH050 FX, flowers texture.
# DM060 institute dome texture/lookdev.
# DM080 institute dome texture/lookdev.
# WD735 institute dome texture/lookdev.

#manheim
# GF124_030 F18 jet texture/lookdev
# RV021_070 scorpion texture/lookdev
# RV021_080 scorpion texture/lookdev

#vulcan
#### TS010 FX. snow flake animation.
# TS030 FX.
# TS040 FX.
# TS090 FX.
# SH400 lover Textureing.
# OA130 environment textureing.
# OA145 environment textureing.
# BA140 environment textureing.
# BA145 environment textureing.
#### MH610 environment textureing.
# MH570 environment textureing.
# MH900 environment textureing.


def cleanStats():
    maxSubdiv = 8
    #var
    dirs = []
    dirtyFiles=[]
    lambertOnes=[]
    noneMipmapFiles=[]
    goodExts = [".exr", ".hdr"]


    #textures check
    fileList = mc.ls(type = "file")
    for f in fileList:
        
        fPath = mc.getAttr(f+".fileTextureName")
        fileExt = os.path.splitext(fPath)[-1]
        if fileExt not in goodExts:
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

    if len(noneMipmapFiles)>0:
        print "==================================="
        print " none mipmap texture filter found."
        print "==================================="
        for f in noneMipmapFiles:
            print f

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

    #Vray shader Checks..
    #subdiv check
    vrayMtls = mc.ls(type = "VRayMtl")
    print "----------------------------------------"
    print " checking vray shader settings ..."    
    print "----------------------------------------"
    for mat in vrayMtls:
        rflSub = mc.getAttr(mat+".reflectionSubdivs")
        rfraSub = mc.getAttr(mat+".refractionSubdivs")
        if rflSub > maxSubdiv:
            print mat, "reflection subdiv: ", rflSub

        if rfraSub > maxSubdiv:
            print mat, "refraction subdiv: ", rfraSub


cleanStats()




##file path replace
##file path replace
oldPath = "/X/projects/vikings3/SHOTS/PROPS/lib/textures/BALLISTAE_BOLT/BALLISTAE_BOLT_tex_fullres/v002"
newPath = "new"

dirs = []
fileList = mc.ls(type = "file")
print "Found", str(len(fileList)), "files in the scene."
for f in fileList:
    fPath = mc.getAttr(f+".fileTextureName")
    dirPath = os.path.split(fPath)[0]
    
    if oldPath in dirPath:
        print fPath
        newDir = fPath.replace(oldPath, newPath)
        print newDir
        mc.setAttr(f+".fileTextureName", newDir, type="string")


##file all replace
oldPath = "/X/projects/vikings3/SHOTS/PARIS_ARMY/lib/textures/FRANK_WARRIOR_A/FRANK_WARRIOR_A_tex_fullres/v001/frankWarrior_A_rfl_ncdh_<UDIM>.exr"
newPath = "/X/projects/vikings3/SHOTS/PARIS_ARMY/lib/textures/FRANK_WARRIOR_A/FRANK_WARRIOR_A_tex_fullres/v002/frankWarrior_A_rfl_ncdh_<UDIM>.exr"

dirs = []
fileList = mc.ls(type = "file")
print "Found", str(len(fileList)), "files in the scene."
for f in fileList:
    fPath = mc.getAttr(f+".fileTextureName")
    if fPath == oldPath:
        print fPath
        print "set to new path: ", newPath
        mc.setAttr(f+".fileTextureName", newPath, type="string")



#!/usr/bin/python2.6
import os, sys, re
from PyQt4 import uic

uicFile = ""
outputFile = ""
def compile(inputfile, outputfile):
    uicFile = file(inputfile)
    pyFile  = file(outputfile,'w')
    uic.compileUi( uicFile, pyFile )
    uicFile.close()
    pyFile.close()

compile(uicFile, outputFile)






for i in mc.listAttr("sceneManagerScriptNode"):
    print i





import maya.cmds as mc

#bounding objects
mc.createNode("boundingObject")
mc.connectAttr("boundingObject2.outData", "attributeTransfer1.boundingObjects[2]")
mc.connectAttr("boundingObject2.outParentMatrix", "attributeTransfer1.boundingObjects[2].boundParentMatrix")
mc.connectAttr("transform1.worldMatrix[0]", "boundingObject2.inParentMatrix")

#attr transfer
mc.createNode("attributeTransfer")


#data container
mc.createNode("arrayDataContainer")
mc.createNode("arrayToPointColor")


print mc.ls(type="attributeTransfer")


import maya.cmds as mc
mc.select(cl=True)
for i in range(0, mc.polyEvaluate("polySurfaceShape1", v=True)):
    if i == 50:
        mc.select("polySurfaceShape1.vtx["+str(i)+"]", add=True)
        mc.polyColorPerVertex( rgb=(0, 0, 1) )



import maya.cmds as mc
EXBAND_RANGE = 2
#selVerts = mc.ls(sl=True)
#print selVert
#comp = mc.polyListComponentConversion(selVerts, fv=True, tf=True)
for t in range(0,EXBAND_RANGE):
    selVerts = mc.ls(sl=True)
    comp = mc.polyListComponentConversion(selVerts, fv=True, tf=True)
    for i in comp:
        v = mc.polyListComponentConversion(i, ff=True, tv=True)
        mc.select(v, add=True)
    

#LUNA VIEWPORT 2 TESTS
#lightri
#light type tag enable and disable
import maya.cmds as mc

def setHeighQuality():
    #anit-aliasing on
    mc.setAttr("hardwareRenderingGlobals.multiSampleEnable", 1)
    mc.setAttr("hardwareRenderingGlobals.multiSampleCount", 16)
    mc.setAttr("hardwareRenderingGlobals.ssaoEnable", 1)
    #set AO
    mc.setAttr("hardwareRenderingGlobals.multiSampleEnable", 1)
    mc.setAttr("hardwareRenderingGlobals.multiSampleCount", 16)

setHeighQuality()


#reconFile = '/USERS/chichang/Documents/DIRK_SUIT_recon.json'
#reconFile = '/USERS/chichang/Documents/DIRK_SUIT_recon.json'

def sandboxLookdevPublish(q=False, ignoreIndex = False, fileName="temp_recon.json", shaderNamae = "temp_shaders.mb"):
    '''
    write out all child mesh shader connection.
    Ignores all namespaces
    '''
    import json
    import os
    
    #selection
    root_grp = mc.ls(sl=True)
    #check selection
    if len(root_grp) < 1:
        mc.warning("please select source.")
        return

    #user shader recon dir
    userDir = os.getenv("USER_SHOT_DIR")
    mayaDataDir = os.path.join(userDir, "maya/data")
    reconFile = os.path.join(mayaDataDir, fileName)
    shaderFile = os.path.join(mayaDataDir, shaderNamae)
    print "writing recon file " + fileName + " to " + reconFile
    print "writing shader file " + shaderNamae + " to " + shaderFile

    #only one grp for now. addin loop later
    source = root_grp[0]
    print "root selected: ", source

    #get all mesh shapes
    all_source_shape = mc.listRelatives(source, ad=True, type = "mesh")

    #init data
    shaderReconDict = {}
    exportSG = []

    #looping through src shape
    for source_shape in all_source_shape:
        
        #ignor namespaces
        clean_source_name = source_shape.split(":")[-1]
        
        #get connected SG name
        srcSGName = mc.listConnections(source_shape, type = "shadingEngine")[0]
        print clean_source_name + "==>>" + srcSGName

        #add to dict
        shaderReconDict[source_shape]=srcSGName
        
        #add shading group to export
        if srcSGName not in exportSG:
            exportSG.append(srcSGName)

    #writeout recon file
    print "writing recon file ..."
    data = shaderReconDict
    with open(reconFile, 'w') as outfile:
        json.dump(data, outfile)
    print "writing recon file succesful: ", reconFile
    
    #exporting shaders
    print "exporting shaders: ", exportSG
    mc.select(cl=True)
    for sg in exportSG:
        #hack.. select it. todo: find better way
        mc.select(sg, ne=True, add=True)
    print "exporting shaders to: " + shaderFile
    
    #export shaders
    mc.file( shaderFile, op="v=0", typ="mayaBinary", pr=True, es=True)
    print "writing shader file succesful: ", shaderFile
    
    #done
    print "lookdev published to sandbox."
    

sandboxLookdevPublish()


def getAssName(s):
    assName = ""
    clean_ass_name = s.split(":")[-1]
    ass_name_list = clean_ass_name.split("_")
    for a in ass_name_list:
        if a.isupper():
            assName += a+"_"
    return assName[:-1]

def shaderRecon(assetName=None,fileName="temp_recon.json", shaderNamae = "temp_shaders.mb"):
    
    import json
    import os

    root_grp = mc.ls(sl=True)
    if len(root_grp) < 1:
        mc.warning("please select target.")
        return

    target = root_grp[0]
    print "target: ", target
    
    #get asset name
    if not assetName:
        assetName = getAssName(target)
    print "asset is: " + assetName
    
    #dir setup
    userName = os.getenv("USER")
    showDir = os.getenv("SHOW_DIR")
    shotDir = os.path.join(showDir, "SHOTS", assetName)
    userDir = os.path.join(shotDir, userName)
    mayaDataDir = os.path.join(userDir, "maya/data")
    print "getting data from: " + mayaDataDir
    reconFile = os.path.join(mayaDataDir, fileName)
    shaderFile = os.path.join(mayaDataDir, shaderNamae)
    
    print "recon file:  " + reconFile
    print "shader file: " + shaderFile

    #check if file exists
    if os.path.isfile(reconFile)==False or os.path.isfile(shaderFile)==False:
        print "no lookdev found!!"

    #reconnectin
    #import shaders
    fileImported = mc.file(shaderFile, i=True, mergeNamespacesOnClash=False)
    print "shader imported from: " + shaderFile


    #get all mesh shapes
    all_target_shape = mc.listRelatives(target, ad=True, type = "mesh")
    print all_target_shape

    #json
    try:
        json_data = open(reconFile)
        data = json.load(json_data)
    except:
        print "error loading recon file."
        pass

    for name, path in data.iteritems():
        for a in all_target_shape:
            if name in a:
                mc.sets(a,e = 1, forceElement = path)
                print " shader assigned: ", name, " ==>> ", path
  
    #done
    print "shader recon finished."

shaderRecon()
    



    #json
    try:
        json_data = open(reconFile)
        data = json.load(json_data)
    except:
        print "error"
        pass

    for name, path in data.iteritems():
        
        print name, path

        mc.sets(name,e = 1, forceElement = path)
        print "matching shape: ", name, " shader ", path

        #assing shader
        #self.addBookmark(path, name)


        '''
        #find if shape matches
        for target_shape in all_target_shape:
            
            clean_target_name = target_shape.split(":")[-1]
            print clean_target_name
            if ignoreIndex:
                clean_target_name = removeNameIndexes(clean_target_name)
                #print clean_target_name

            if clean_source_name == clean_target_name:
                
                #match shader.
                matSGName = mc.listConnections(source_shape, type = "shadingEngine")
                print "matching shape: ", source_shape, " shader ", matSGName[0], " to ", target_shape

                mc.sets(target_shape,e = 1, forceElement = matSGName[0])
                source_found.append(target_shape)
        '''

import os
def initMmesh():
    #attr transfer
    mc.createNode("attributeTransfer")
    #data container
    mc.createNode("arrayDataContainer")
    mc.createNode("arrayToPointColor")

    print "initialize mesh"

def addBObjToAttrTransfer(bObj, attrTrans):
    
    print "conndection ", bObj, " to ", attrTrans

    allConnections = mc.listConnections(attrTrans, c=True)
    curIndex = None
    for c in allConnections:
        #Sortit!!!
        if "boundingObjects" in c:
            index = c.split("[")[-1][0]
            curIndex = index
    if curIndex:
        index2Connect = int(curIndex)+1
    else:
        index2Connect = 0

    print "connecting bounding object to slot " + str(index2Connect)
    
    #connecting bounding object
    mc.connectAttr(bObj+".outData", attrTrans+".boundingObjects["+str(index2Connect)+"]")
    mc.connectAttr(bObj+".outParentMatrix", attrTrans+".boundingObjects["+str(index2Connect)+"].boundParentMatrix")

def removeInfluence():
    print "removing bounding object influence."
    

def addInfluenc():
    allSelected = mc.ls(sl=True)
    allBObj = []
    allColorTrans = []
    
    for i in allSelected:
        nodeType = mc.nodeType(i)
        if nodeType == "boundingObject":
            allBObj.append(i)
        elif nodeType =="attributeTransfer":
            allColorTrans.append(i)

        print "all bounding object selected: ", allBObj
        print "all attributeTransfer selected: ", allColorTrans
        
    #connecting bobj to attr transfer
    for b in allBObj:
        #connect to a
        for a in allColorTrans:
            addBObjToAttrTransfer(b,a)

def doTransfer(transfer):
    nodesToDisable = ["arrayDataContainer","attributeTransfer"]
    for n in nodesToDisable:
        allNodes = mc.ls(type=n)
        #disable aray data container
        for t in allNodes:
            if transfer:
                mc.setAttr(t+".envelope", 1)
            
            if not transfer:
                mc.setAttr(t+".envelope", 0)

doTransfer(True)





##Cam seq render

##Cam seq render
import maya.cmds as mc
import maya.mel as mel
import subprocess

def camSeqRender(sh):
    allshots = mc.sequenceManager(lsh=True)
    print allshots
    for rs in allshots:
        if rs == sh:
            s=rs

    print s
    
    renderCam = mc.shot(s, cc=True, q=True)
    startTime = mc.shot(s, st=True, q=True)
    endTime = mc.shot(s, et=True, q=True)
    
    #get it for nuke 
    seq_startTime = mc.shot(s, sst=True, q=True)
    seq_endTime = mc.shot(s, set=True, q=True)
    
    offsetTime = int(seq_startTime-startTime)
    
    print s, startTime, endTime,"(",seq_startTime, seq_endTime, ")", renderCam

    print "start rendering: ", renderCam
    
    camTransform = mc.listRelatives(renderCam, p=True)[0]

    #mel.eval("lookThroughModelPanel %s modelPanel4;"%(renderCam))

    mel.eval('currentTime %s ;'%(startTime))
    while(startTime <= endTime):
        mel.eval('renderWindowRender redoPreviousRender renderView;')
        startTime += 1
        mel.eval('currentTime %s ;'%(startTime))
    
    callString = "mv /X/projects/luna/SHOTS/"+os.getenv("SHOT")+"/chichang/images/elements/tmp/ /X/projects/luna/SHOTS/"+os.getenv("SHOT")+"/chichang/images/elements/"+camTransform+"_"+str(offsetTime)+"/"
    mycmd=subprocess.Popen(callString, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error=mycmd.communicate()
    
camSeqRender("shot02")




startTime=None
endTime=None
import maya.mel as mel
mel.eval('currentTime %s ;'%(startTime))
while(startTime < endTime):
    mel.eval('renderWindowRender redoPreviousRender renderView;')
    startTime += 1
    mel.eval('currentTime %s ;'%(startTime))







from arnold import *
import random

ass_file = "/Path/To/Ass/File.ass"

userAttrToFind = "idGroup"

#load the ass file
AiBegin()
AiMsgSetConsoleFlags(AI_LOG_ALL)
AiASSLoad(ass_file, AI_NODE_ALL)

# Iterate over all shape nodes
shapeIter = AiUniverseGetNodeIterator(AI_NODE_SHAPE);

while not AiNodeIteratorFinished(shapeIter):
    
    node = AiNodeIteratorGetNext(shapeIter)

    #check if this node is a polygon mesh.
    if AiNodeIs(node, "polymesh"):

        #find if user attribute is found on the shape
        userPramIter = AiNodeGetUserParamIterator(node)

        while not AiUserParamIteratorFinished(userPramIter):

            #find the user attribte
            entry = AiUserParamIteratorGetNext(userPramIter)
            entryName = AiUserParamGetName(entry)

            if  entryName == userAttrToFind:
                print "found user attribute on shape " + AiNodeGetName(node)
                print entryName, ":", str(AiNodeGetInt(node, userAttrToFind))

                #here is an example of simply setting the attribute to a random number.
                newVal = random.choice([1,2,3,4,5])
                print "setting " + userAttrToFind + " to => " +str(newVal)
                AiNodeSetInt(node, userAttrToFind, newVal)
                
        #end the user Pram loop
        AiUserParamIteratorDestroy(userPramIter)

    else:
        #print "not a polygon mesh"
        pass

#end the shape loop
AiNodeIteratorDestroy(shapeIter)

#save and quit
AiASSWrite(ass_file, AI_NODE_ALL, True)
AiEnd()








import maya.cmds as mc

shadingGroups = mc.ls(type="shadingEngine")

for sg in shadingGroups:
    connectedShader = mc.connectionInfo(sg+".surfaceShader", sfd=True)
    connectedShader = connectedShader.split(".")[0]
    #print sg+ " => " + connectedShader
    if sg != connectedShader+"SG":
        try:
            mc.rename(sg, connectedShader+"SG")
            print "renaming " + sg + " => " + connectedShader+"SG"
        except:
            print "can not rename shading group: " + sg





allStandin = mc.ls(type = "aiStandIn")

for i in allStandin:
    print i
    mc.setAttr(i+".primaryVisibility", 0)












import maya.cmds as mc
mesh = mc.ls(sl=True)[0]
if mc.nodeType(mesh)=="transform":
    meshShape = mc.listRelatives(s=True)[-1]
else:
    meshShape = mesh
print "selected mesh: ", meshShape

furShapes = mc.ls(type="pgYetiMaya")
groomShapes = mc.ls(type="pgYetiGroom")

print furShapes
print groomShapes

#connect fur
for f in furShapes:
    print "connecting", f, "to mesh."
    try:
        mc.connectAttr(meshShape+".worldMesh[0]", f+".inputGeometry[0]")
    except:
        print "error connecting ", f

#connect groom
for g in groomShapes:
    print "connecting", g, "to mesh."
    try:
        mc.connectAttr(meshShape+".worldMesh[0]", g+".inputGeometry")
    except:
        print "error connecting ", g




def name_clash():
    import maya.cmds as mc
    geo = mc.ls(type="mesh")
    a = []
    for i in geo:
        name = i.split(":")[-1]
        #print name
        if name in a:
            print "AHHH!!!", name
        else:
            a.append(name)
    print a








toInstance = "ArnoldStandIn"
import maya.cmds as mc
counter = 0
max = None
trees = mc.ls(type="transform")

if not max:
    max = len(trees)

print "building ", max, "trees ..."

for i in trees:
    if "tree_standin" in i:
        trans = mc.xform(i, t=True, q=True, ws = True)
        rot = mc.xform(i, ro=True, q=True)
        sca = mc.xform(i, s=True, q=True)

        new = mc.instance(toInstance)
        
        mc.xform(new, t=trans)
        mc.xform(new, ro=rot)
        mc.xform(new, s=[sca[0]*2, sca[1]*2, sca[2]*2])
        
        counter += 1
        
        if counter > max:
            break





import maya.cmds as mc
import random

#set range here
randomRange = 50
searchString = None

def setAllVMeshOffset(randomRange, searchString):
    vrayMeshList = mc.ls(type = "VRayMesh")
    randMax = randomRange
    randMim = -randomRange
    for m in vrayMeshList:
        val =random.randint(randMim, randMax)
        
        if searchString:
            if searchString in m:
                print "setting ", m, " offset value to ", val
                mc.setAttr(m+".animOffset", val)
                mc.setAttr(m+".animType", 2)
        else:
            print "setting ", m, " offset value to ", val
            mc.setAttr(m+".animOffset", val)
            mc.setAttr(m+".animType", 2)

#run
setAllVMeshOffset(randomRange, searchString)




#replace swap texture path
import maya.cmds as mc
new_file = "/mnt/X/projects/mena/SHOTS/TRANQUILANDIA/lib/textures/COCA_PLANT_A/COCA_PLANT_A_tex_fullres/v002/GreenAshLeaf_single.exr"
old_file = "/mnt/X/projects/mena/SHOTS/TRANQUILANDIA/lib/textures/COCA_PLANT_A/COCA_PLANT_A_tex_fullres/v001/GreenAshLeaf.exr"
#old_file = "/mnt/X/projects/mena/SHOTS/TRANQUILANDIA/lib/textures/COCA_PLANT_A/COCA_PLANT_A_tex_fullres/v001/GreenAshLeaf.exr"
files = mc.ls(type="file")
for i in files:
    file_path = mc.getAttr(i+".fileTextureName")
    if file_path == old_file:
        print i
        mc.setAttr(i+".fileTextureName", new_file, type="string")


#setp through sub-frames
import maya.cmds as mc
import time
ct = mc.currentTime(q=True)
print ct
step = 0.01
nt=ct
for i in range(0, 100):
    time.sleep(0.01)
    nt = nt+step
    mc.currentTime(nt, e=True)




#############NUKE###############

##########################################
#	p_Noise3D
##########################################
set cut_paste_input [stack 0]
version 9.0 v6
push $cut_paste_input
Expression {
 temp_name0 fBmNoise
 temp_expr0 fBm((r+offset.x)*1/size.x,(g+offset.y)*1/size.y,(b+offset.z)*1/size.z,octaves,lacunarity,gain)*.5+0.5
 temp_name1 turbNoise
 temp_expr1 turbulence((r+offset.x)*1/size.x,(g+offset.y)*1/size.y,(b+offset.z)*1/size.z,octaves,lacunarity,gain)
 channel0 alpha
 expr0 "parent.useAlpha && a == 0 ? 0 : (noisetype==0?fBmNoise:noisetype==1?turbNoise:0)"
 name Expression3
 selected true
 xpos 390
 ypos -419
}
##########################################



###########COCA POSTBUILD
import maya.cmds as mc
mtls = mc.ls(type="VRayMtl")
for i in mtls:
    if "COCA" in i:
        print i
        mc.setAttr(i+".reflectionSubdivs", 2)
        mc.setAttr(i+".reflectionColorAmount", 0)
    if "TREE" in i:
        print i
        mc.setAttr(i+".reflectionSubdivs", 2)
        mc.setAttr(i+".reflectionColorAmount", 0)
        
wrapper = mc.ls(type="VRayMtlWrapper")
for i in wrapper:
    if "COCA" in i:
        print i
        mc.setAttr(i+".receiveGIMultiplier", 1)
    if "TREE" in i:
        print i
        mc.setAttr(i+".receiveGIMultiplier", 1)

vmesh = mc.ls(type="VRayMesh")
for i in vmesh:
    mc.setAttr(i+".showBBoxOnly", 1)
    
def setAllFileFilter():
    allFile = mc.ls(type = "file")
    for i in allFile:
        mc.setAttr(i+".filterType", 0)
setAllFileFilter()

'''
import maya.cmds as cmds

# Close ports if they were already open under another configuration
try: cmds.commandPort(name=":7001", close=True)
except: cmds.warning('Could not close port 7001 (maybe it is not opened yet...)')
try: cmds.commandPort(name=":7002", close=True)
except: cmds.warning('Could not close port 7002 (maybe it is not opened yet...)')

# Open new ports
cmds.commandPort(name=":7001", sourceType="mel")
cmds.commandPort(name=":7002", sourceType="python")
'''


'''
from DefinedAssets import DefinedAssets
from Asset import Asset

da = DefinedAssets("testing","GOTHAM", shot_only=False)
all_assets = da.assets()

for asset in all_assets:
    print asset

#a = da.getAsset("TRAILER_C_lookdev")
#print a
#print a.name()
#print a.id()


from XAssets import assets
rig_asset = assets.RigAsset()
print rig_asset
print rig_asset.setAssetName("GOTHAM_rig")
print rig_asset.getAssetName()
print rig_asset.getCategory()
print rig_asset.get

#print rig_asset.info()


tt_rig_asset = Asset()
tt_rig_asset.setName("TURNTABLE_rig")
tt_rig_asset.setCategory("maya_rig")
ld_asset.setDirFlag("one")
ld_asset.setPublishDir("")
ld_asset.setType(define_attrs.get('type'))
ld_asset.setDescription(description)
ld_asset.setExtension(define_attrs.get('extension'))

print tt_rig_asset
'''










'''
oiio_iv
export LD_LIBRARY_PATH=/USERS/chichang/lib64:/X/projects/testing/SHOTS/_default/chichang/lib64:/X/projects/testing/SHOTS/_default/lib/lib64:/X/projects/testing/lib64:/X/tools/liblinux:/X/tools/binlinux/arnold/arnold-4.2.3.1/bin:/X/tools/binlinux/apps/peregrine/yeti-UNK/maya2015/bin:/X/tools/python/bin/linux_python2.7/lib:/X/tools/binlinux/vray/maya2015/vray_3.05.04.25341/maya/lib:/X/tools/binlinux/apps/RisingSunResearch/cineSpace:/X/tools/binlinux/sesi/hfs14.0.258/dsolib:/X/tools/binlinux/apps/OFX/Plugins/genarts/SapphireOFX/lib64:/X/tools/XRender/lib:/usr/lib64:/usr/lib:/lib:/X/tools/packages/gcc-4.1/glew/glew-1.10.0/lib64

'''

from XAssets import assets
import os
#help(assets)

assets = assets.CategoryManager()

asset = assets.get_asset("render")
#print asset
#help(asset)
asset.setShow("maury")
asset.setShot("109_0210")
asset.setAssetName("GRENADE_BEAUTY")

print asset.parents()
print asset.assetId()
print asset.getAssetName()
print asset.getPublishDir()
print asset.getCategory()
print asset.getName()
print asset.getPublishVersion()
print asset.latestVersion()
print asset.isPublished()


#help(assets)

asset = assets.get_asset("render")

#print asset
#help(asset)
asset.setShow(os.getenv("SHOW"))
asset.setShot(os.getenv("SHOT"))
asset.setAssetName("DUCK_BEAUTY")

asset.setDailies(d=False)
asset.setOperation(op=1) #COPY
asset.setPublishDir("images/ltm/DUCK")
asset.setPublishVersion(asset.getPublishVersion())
asset.setSource("/X/projects/testing/SHOTS/ARNOLD/chichang/images/elements/Tfi_Test/v005/BEAUTY/Tfi_Test_BEAUTY_v005.%04d.exr")
#/X/projects/maury/SHOTS/109_0360/chichang/images/elements/lighting/v005/SPECULAR/109_0360_lighting_v005_SPECULAR.%04d.exr
print asset.getPublishVersion()
print asset.getPublishDir()
print asset.getPublishDestination()
print asset.getPublishPath()
print asset.getName()

print asset.isPublished()
#Before publishing, create the asset define name.
asset.prePublish()
#asset.publish()






from XAssets import assets
import os
#help(assets)

assets = assets.CategoryManager()

asset = assets.get_asset("texture")
#print asset
#help(asset)
asset.setShow("maury")
asset.setShot("GRENADE")
asset.setAssetName("GRENADE_tex_src")

print asset.parents()
print asset.assetId()
print asset.getAssetName()
print asset.getPublishDir()
print asset.getCategory()
print asset.getName()
print asset.getPublishVersion()
print asset.latestVersion()
print asset.isPublished()


#help(assets)

asset = assets.get_asset("texture")

#print asset
#help(asset)
asset.setShow(os.getenv("SHOW"))
asset.setShot(os.getenv("SHOT"))
asset.setAssetName("DUCK_tex_src")

asset.setDailies(d=False)
asset.setOperation(op=1) #COPY
asset.setPublishDir("textures/DUCK") # textures/ASSET
asset.setPublishVersion(asset.getPublishVersion())
asset.setSource("/X/projects/testing/SHOTS/ARNOLD/chichang/textures/female")
asset.addSource("/X/projects/testing/SHOTS/ARNOLD/chichang/textures/male")
#/X/projects/maury/SHOTS/109_0360/chichang/images/elements/lighting/v005/SPECULAR/109_0360_lighting_v005_SPECULAR.%04d.exr
print asset.getPublishVersion()
print asset.getPublishDir()
print asset.getCategory()
print asset.getPublishDestination()
#print asset.getPublishPath()
print asset.getName()

print asset.isPublished()
#Before publishing, create the asset define name.
asset.prePublish()
asset.publish()
print asset.isPublished()
