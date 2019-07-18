# -*- coding: utf-8 -*-
import os, sys, json, socket, time, threading, ftplib 
from subprocess import PIPE, Popen

import zipfile 
import shutil

def Unzip(src, dest):
    shutil.unpack_archive(src, dest)

def Zip(src, dest, format): 
    if not os.path.isdir(src):
        print("archive path need folder type ")
        return
    shutil.make_archive(dest, format, src)

event = threading.Event()
serverIP = ""
#多网卡情况下，根据前缀获取本地IP
def GetLocalIPByPrefix(prefix):
    localIP = ''
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if ip.startswith(prefix):
            localIP = ip
     
    return localIP

# 下载单个文件
def DownLoadFile(ftpInst, LocalFile, RemoteFile):  
        file_handler = open(LocalFile, 'wb')
        ftpInst.retrbinary('RETR ' + RemoteFile, file_handler.write)
        file_handler.close()
        print("RemoteFile:{}        Saveing To: {}".format(RemoteFile, LocalFile))
        return True

# 下载整个目录下的文件
def DownLoadFileTree(ftpInst, LocalDir, RemoteDir):  

    if not os.path.exists(LocalDir):
        os.makedirs(LocalDir)
    ftpInst.cwd(RemoteDir)
    RemoteNames = ftpInst.nlst()

    for file in RemoteNames:
        Local = os.path.join(LocalDir, file)
        if file.find(".") == -1:
            if not os.path.exists(Local):
                os.makedirs(Local)
            DownLoadFileTree(ftpInst, Local, file)
        else:
            DownLoadFile(ftpInst, Local, file)
    ftpInst.cwd("..\\")
    return

def loginFTP(ipAddr):
    ftpInst = ftplib.FTP()
    ftpInst.connect(ipAddr,2121)
    ftpInst.login("gsrp_worker", "gsrp_Passw0rd")
    return ftpInst

def downloadWorkerFiles(ipAddr):
    ftpInst = loginFTP(ipAddr)
    DownLoadFileTree(ftpInst,r"D:\GSRP_Server\GSRP_Worker",r".\GSRP_Worker")
    ftpInst.quit()

    if not os.path.exists(r"D:\GSRP_Server\python27.zip"):
        ftpInst = loginFTP(ipAddr)
        DownLoadFile(ftpInst,r"D:\GSRP_Server\python27.zip",r".\python27.zip")
        ftpInst.quit()
    if not os.path.exists(r"D:\GSRP_Server\Pandora\Python27") or not os.path.exists(r"D:\GSRP_Server\Pandora\PythonLibs"):
        Unzip(
            r"D:\GSRP_Server\python27.zip", 
            r"D:\GSRP_Server\Pandora"
        )

    ftpInst = loginFTP(ipAddr)
    DownLoadFileTree(ftpInst,r"D:\GSRP_Server\Pandora\Plugins",r".\Pandora\Plugins") 
    ftpInst.quit()

    ftpInst = loginFTP(ipAddr)
    DownLoadFileTree(ftpInst,r"D:\GSRP_Server\Pandora\Scripts",r".\Pandora\Scripts")
    ftpInst.quit()

def tryLogin(ipAddr):                #参数(主机名，字典文件)
    global serverIP
    try:
        with ftplib.FTP() as ftpInst:  #以主机名为参数构造Ftp对象
            ftpInst.connect(ipAddr,2121)
            ftpInst.login("gsrp_worker", "gsrp_Passw0rd")  
            print("FOUND FTP SERVER! IP={}".format(ipAddr))
            serverIP = ipAddr
            ftpInst.close()

            downloadWorkerFiles(ipAddr)
    
            event.set()
    except:
        # 产生异常表示没有登录成功，这里我们不用管它，继续尝试其他用户名、密码
        pass

def Sniffing_all(ip): 
    pre_ip = (ip.split('.')[:-1])
    # 设置线程组
    threads = []
    for i in range(1,256):
        add = ('.'.join(pre_ip)+'.'+str(i))
        th = threading.Thread(target=tryLogin, args=(add,))
        # 添加到线程组
        threads.append(th)
    # 开启线程
    for thread in threads:
        thread.start()

def GetRunningFile():
    localIP = GetLocalIPByPrefix('192.168')
    print("localIP={}".format(localIP))
    Sniffing_all(localIP)

def main():
    global serverIP

    if not os.path.exists("D:\\Autodesk"):
        shutil.copytree("C:\\Progra~1\\Autodesk","D:\\Autodesk")
        
    GetRunningFile()
 
    event.wait()
    
    print("########################################")
    print("Start PandoraSlave Running...")
    print("See More Detail In Renderhandler.")
    print("########################################")
    
    cmd = ' '.join([r"D:\GSRP_Server\Pandora\Python27\python.exe", r"D:\GSRP_Server\GSRP_Worker\run.py",serverIP])
    p1 = Popen(
        args=cmd,       # args='r"绝对路径"', 
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