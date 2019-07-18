# -*- coding: utf-8 -*-
import os, sys, json, socket, time, threading, ftplib 
from subprocess import PIPE, Popen


def createUserPrefs(rootPath):

    from win32com.shell import shell, shellcon
    cRoot = rootPath
    wsPath = os.path.join(cRoot, "Workstations", "WS_" + socket.gethostname())
    sPath = os.path.join(cRoot, "Slaves", "S_" + socket.gethostname())
    localRep = os.path.join(shell.SHGetFolderPath(0, shellcon.CSIDL_PERSONAL, None, 0), "PandoraRepository")

    configPath = os.path.join(os.environ["userprofile"], "Documents", "Pandora", "Pandora.json")
    if not os.path.exists(os.path.dirname(configPath)):
        os.makedirs(os.path.dirname(configPath))

    uconfig = {
        "globals": {
            "localMode": True,
            "rootPath": cRoot,
            "repositoryPath": localRep,
            "checkForUpdates": False
        },
        "submissions": {
            "submissionPath": wsPath,
            "userName": ""
        },
        "slave": {
            "enabled": False,
            "slavePath": sPath
        },
        "coordinator": {
            "enabled": False,
            "rootPath": cRoot
        },
        "renderHandler": {
            "refreshTime": 5,
            "logLimit": 500,
            "showCoordinator": True,
            "autoUpdate": True,
            "windowSize": ""
        },
        "dccoverrides": {
        },
        "lastUsedSettings": {
        }

    }

    with open(configPath, 'w') as confFile:
        json.dump(uconfig, confFile, indent=4)
        print("Save Config to {}:".format(configPath))
        print("uconfig: {}".format(uconfig))

def main():
    if len(sys.argv[1]) == 1:
        print("Please Specify Server Address!")
        return

    serverName = sys.argv[1]
    rootPath = os.path.join('\\\\'+serverName, 'GSRP_Server\\GSRP_Coordinator\\')
    createUserPrefs(rootPath)
    # start PandoraSlave
    dir0 = r"D:\GSRP_Server\Pandora\Scripts\PandoraSlave.py"
    pandoraSlave = ' '.join([r"D:\GSRP_Server\Pandora\Python27\PandoraSlave.exe", dir0])
    print("Start Run Worker : {}".format(pandoraSlave))
    p1 = Popen(
        args=pandoraSlave,       # args='r"绝对路径"', 
        # stdout = PIPE,    # 重定向输出的设备。把程序里的结果不输入屏幕上，而是重定向到终端上。
        # stderr = PIPE,    
        shell=True,
    )

    output, err = p1.communicate()    
    if output == None:
        output = "(NO OUTPUT. Please Redirect stdout&stderr)"
    print(":-------------------------:")
    print("pandoraSlave Output:",output)
    print(":-------------------------:")
    print("pandoraSlave Err:",err)
    print(":-------------------------:")

if __name__ == '__main__':
    main()