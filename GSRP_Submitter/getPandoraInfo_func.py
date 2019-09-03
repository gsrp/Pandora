import json
import os

class slaveProperty:
    slaveinfo="slaveinfo"
    status = "status"
    curjob ="curjob"
    cpucount="cpucount"
    ram ="ram"
    slaveScriptVersion = "slaveScriptVersion"

class submitSlaveProperty:
    slaves = "slaves"
    status = "status"
    coordinator = "coordinator"
    curjob="curjob"
    renderer = "renderer"
    cpucount = "cpucount"
    ram = "ram"
    slaveScriptVersion="slaveScriptVersion"


class projProperty:
    information="information"
    projectName="projectName"
    submitDate="submitDate"
    program="program"
    programVersion="programVersion"
    submitWorkstation="submitWorkstation"
    jobtasks = "jobtasks"



class submitProjProperty:
    projects="projects"
    status="status"
    submitDate = "submitDate"
    program="program"


def getSlaveInfo(path):
    try:
        allfilelist = os.listdir(path)
        slaveDict={}
        slaveObjDict = {}
        for file in allfilelist:
            print "file: ",file
            filepath = os.path.join(path, file)
            if os.path.isdir(filepath):
                slaveName = file
                slaveSettingsPath = os.path.join(filepath, "slaveSettings_"+ file[2:]+".json")
                print slaveSettingsPath
                if os.path.exists(slaveSettingsPath):
                    file = open(slaveSettingsPath, "r")
                    s = json.load(file)
                    curSlaveInfo = s[slaveProperty.slaveinfo]
                    slaveInfoDict={}
                    slaveInfoDict[submitSlaveProperty.coordinator] = os.environ['COMPUTERNAME']
                    slaveInfoDict[submitSlaveProperty.status] = str(curSlaveInfo[slaveProperty.status])
                    slaveInfoDict[submitSlaveProperty.curjob] = str(curSlaveInfo[slaveProperty.curjob])
                    slaveInfoDict[submitSlaveProperty.ram] = curSlaveInfo[slaveProperty.ram]
                    slaveInfoDict[submitSlaveProperty.cpucount] = curSlaveInfo[slaveProperty.cpucount]
                    slaveInfoDict[submitSlaveProperty.slaveScriptVersion] = str(curSlaveInfo[slaveProperty.slaveScriptVersion])
                    slaveInfoDict[submitSlaveProperty.renderer] = "Redshift v1.4.2"
                    slaveObjDict[slaveName] = slaveInfoDict
                else:
                    print (slaveSettingsPath + " not exist !")
        slaveDict[submitSlaveProperty.slaves] = slaveObjDict
        return (True, slaveDict)
    except Exception as err:
        print("getSlaveInfo Except Error : " +str(err))
        return (False,slaveDict)

def getAllProj(path):
    try:
        allfilelist = os.listdir(path)
        projDict = {}
        projObjDict = {}
        for file in allfilelist:
            filepath = os.path.join(path, file)
            if os.path.isdir(filepath):
                pandoraJobPath = os.path.join(filepath, "PandoraJob.json")
                if os.path.exists(pandoraJobPath):
                    file = open(pandoraJobPath, "r")
                    s = json.load(file)
                    curProjInfoDict = s[projProperty.information]
                    curJobTaskDict = s[projProperty.jobtasks]
                    projName = curProjInfoDict[projProperty.projectName]
                    projInfoDict = {}
                    # 根据task的信息计算出完成情况
                    programInfo = curProjInfoDict[projProperty.program] + curProjInfoDict[projProperty.programVersion]
                    projInfoDict[submitProjProperty.program] = programInfo
                    projInfoDict[submitProjProperty.submitDate] = curProjInfoDict[projProperty.submitDate]
                    iJobTaskCount = len(curJobTaskDict.items())
                    iJobTaskFinishedCount = 0
                    for key,value in curJobTaskDict.items():
                        taskStatus = value[2]
                        if taskStatus == "finished":
                            iJobTaskFinishedCount += 1
                        projInfoDict[key] = value
                    status = "finished"
                    if iJobTaskFinishedCount != iJobTaskCount:
                        status = str(iJobTaskFinishedCount)+"/"+str(iJobTaskCount)
                    projInfoDict[submitProjProperty.status] = status
                    projObjDict[projName] = projInfoDict
        projDict[submitProjProperty.projects] = projObjDict
        print("--------------------")
        print(projDict)
        return (True,projDict)
    except Exception as err:
        print("getAllProj Exception Error : " +str(err))
        return (False, projDict)


if __name__ == '__main__':
    print os.environ['COMPUTERNAME']
    #getSlaveInfo("\\\\192.168.50.26\\GSRP_Server\\GSRP_Coordinator\\Slaves")
    #getAllProj("\\\\192.168.50.26\\GSRP_Server\\GSRP_Coordinator\\JobRepository\\Jobs")




