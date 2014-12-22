
import maya.cmds as mc
import shotgun
import os
import MySQLdb, re, sys
import MySQLdb.cursors

show = os.getenv("SHOW")
shot = os.getenv("SHOT")

checkFor = "lookdev_shaders"

wrongVersionSGInUse=[]
shotgunErrorAss=[]

result = []

debug = 0

def triPostCheck():
    # grabbing all vray proxy asset in scene.
    #allAss = mc.ls(type = "VRayMesh")
    allAss = mc.ls(type = "mesh")
    for ass in allAss:
        if debug: print "found vray mesh: ", ass

    allNameSpaces = mc.namespaceInfo(listNamespace=True)

    allSGInUse = []

    for ass in allAss:
        allOutput = mc.listConnections(ass, d=True)
        for outPut in allOutput:
            outNodeType = mc.nodeType(outPut)
            if outNodeType == "shadingEngine":
                if debug: print"found SG in use: ", outPut
                #store all sg in use in list and check if it's the latest.
                if outPut not in allSGInUse:
                    allSGInUse.append(outPut)

    print "\nchecking version for following sg in use:"
    print '\n'.join(allSGInUse) +'\n'

    for sg in allSGInUse:

        if ":" in sg:
            assNameSpace = sg.split(":")[0]
            if assNameSpace in allNameSpaces:
                if debug: print "namespace found: ", assNameSpace
                assVersion = int(getAssVer(assNameSpace))
                if debug: print "asset version: ", assVersion
                
                assLatestVersion = getLatestAssVer(assNameSpace, checkFor)
                if debug: print "shotgun latest version: ", assLatestVersion
                
                if assLatestVersion == 0:
                    shotgunErrorAss.append(sg)
                    continue

                elif(assVersion != assLatestVersion):
                    print "!!!!!!!!!!! WRONG VERSION ?? !!!!!!!!!!!!!!!"
                    wrongVersionSGInUse.append(sg)

        else:
            if debug: print sg, " is root. skipping ..."

    if debug: print "wrong version check: ", wrongVersionSGInUse
    if debug: print "shotgun couldnt find: ", shotgunErrorAss

    if len(wrongVersionSGInUse) > 0:
        for sg in wrongVersionSGInUse:
            for i in mc.listConnections(sg, s=True, sh=True):
                if mc.nodeType(i) == "mesh" and ":" in i:
                    lte = i.split(":")[0]
                    result.append(lte)

        print "==================================================="
        print "the following asset may have old lookdev attached:"
        print "==================================================="
        print '\n'.join(result)

    else:
        print "===================================="
        print "all lookdevs seems to be up to date."
        print "===================================="

    if len(shotgunErrorAss) > 0:
        print "======================================="
        print "fail to find version for the following:"
        print "======================================="
        print '\n'.join(shotgunErrorAss)

def getAssVer(assNameSpace):
    #print "check ass version for ", ass
    assVersion = assNameSpace.split("_")[-1].replace("v", "")
    return assVersion

def getLatestAssVer(assNameSpace, checkFor):
    assName = assNameSpace.split("_"+checkFor)[0]
    print "check", checkFor, "ass version for", assNameSpace
    
    checkAssStr = assName+"_"+checkFor
    
    foundAss = assetFind(show, assName)
    
    AssVersion = foundAss[0]
    AssDir = foundAss[1]
    
    assShot = AssDir.split("SHOTS")[1].split("/")[1]
    if debug: print "asset in shot: ", assShot
    
    sgdict = shotgun.getLastVersion(show, assShot, checkAssStr)
    if debug: print "ghotgun found: ", sgdict
    if debug: print "database latest version: ", AssVersion
    return sgdict[checkAssStr]

    #check and cleanup namespaces

def dbQueryGotham(query):
    try:
        conn = MySQLdb.connect(host="x-database",user="xrender",db="XPublish", cursorclass=MySQLdb.cursors.DictCursor)
    except:
        conn = MySQLdb.connect(host="192.168.212.102",user="xrender",db="XPublish", cursorclass=MySQLdb.cursors.DictCursor)
    finally:
        db = conn.cursor()
        db.execute(query)
        info = db.fetchall()
        db.close()   
        conn.close()
        return info

def assetFind( show, filters, isGlobal = False ):
    latest = {}
    datasets = []
    items = []
    
    definToFind = filters+"_"+checkFor
    
    NY = dbQueryGotham("select shot,asset,publish_dir,version,attributes from publish where publish.show='%s'" %(show))
    if isGlobal:
        TO = dbQueryTO("select shot,asset,publish_dir,version,attributes from publish where publish.show='%s'" %(show))       
    else:
        TO = None
    for dataset in [NY,TO]:
        if dataset:
            datasets.append(dataset)
    for data in datasets:
        for i in range(len(data)):
            item = data[i]
            asset = item['asset']
            pubDir = item['publish_dir'].replace('X:','/X').replace('///','/')
            ver = item['version']
            
            if asset not in latest:
                latest[asset] = [ver,pubDir]
            elif ver > int(latest[asset][0]):
                latest[asset] = [ver,pubDir]

        for k,v in latest.items():
            if k == definToFind:
                if debug: print "found asset in database: ",k, v
                return v

        print "Nothing found that matches", definToFind
        return None


triPostCheck()
