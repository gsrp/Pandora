# -*- coding: utf-8 -*-
import os,time, json, socket
from subprocess import PIPE, Popen
from pyftpdlib.authorizers import DummyAuthorizer 
from pyftpdlib.handlers import FTPHandler 
from pyftpdlib.servers import FTPServer 


def main():
    dir0 = r".\Pandora\Scripts\PandoraSettings.py"
    dir1 = r".\GSRP_Coordinator\Scripts\PandoraCoordinator\PandoraCoordinator.py"
    dir2 = r".\Pandora\Scripts\PandoraRenderHandler.py"

    # start PandoraSettings
    pandoraSettings = ' '.join([r".\Pandora\Python27\python.exe", dir0])

    # start PandoraCoordinator
    pandoraCoordinator = ' '.join([r".\Pandora\Python27\python.exe", dir1]) # r".\Pandora\Python27\python.exe"

    # start monitor
    pandoraRenderHandler = ' '.join([r".\Pandora\Python27\python.exe", dir2])

    p0 = Popen(
        args=pandoraSettings,       # args='r"绝对路径"', 
        # stdout = PIPE,    # 重定向输出的设备。把程序里的结果不输入屏幕上，而是重定向到终端上。
        # stderr = PIPE,    
        shell=True,
    )
    p0.communicate()

    # with open(os.path.join(os.environ["userprofile"], "Documents", "Pandora", "Pandora.json"),'r') as load_f:
    #     conf = json.load(load_f)
    #     rootpath = conf['globals']['rootPath']
    #     fp = open(os.path.join(rootpath,'rootpath.txt'), 'w')
    #     fp.write(rootpath[2:]) # 去掉盘符
    #     fp.close()
    #     load_f.close()

    p1 = Popen(
        args=pandoraCoordinator,       # args='r"绝对路径"', 
        # stdout = PIPE,    # 重定向输出的设备。把程序里的结果不输入屏幕上，而是重定向到终端上。
        # stderr = PIPE,    
        shell=True,
    )
    print("Wait 5s to rising a RenderHandler ... ")
    time.sleep(5)
    p2 = Popen(
        args=pandoraRenderHandler,       # args='r"绝对路径"', 
        # stdout = PIPE,    # 重定向输出的设备。把程序里的结果不输入屏幕上，而是重定向到终端上。
        # stderr = PIPE,    
        shell=True,
    )

    # 实例化用户授权管理 
    try:
        authorizer = DummyAuthorizer() 
        authorizer.add_user( # 该用户用来领取任务
            "gsrp_worker", 
            "gsrp_Passw0rd", 
            os.path.join(os.path.abspath(__file__), os.pardir, os.pardir),  # D:\\GSRP_Server
            perm='elradfmwM') # 添加用户 参数:username,password,允许的路径,权限 

    except Exception as e:
        print("ADD User Fail: {}".format(e))

    # 实例化FTPHandler 
    handler = FTPHandler 
    handler.authorizer = authorizer 
    
    # 设定一个客户端链接时的标语 
    handler.banner = "Welcome GSRP FTP Server." 
    print(handler.banner)
    # handler.masquerade_address = '151.25.42.11'#指定伪装ip地址 
    # #handler.passive_ports = range(60000, 65535)#指定允许的端口范围 
    try:
        address = ('0.0.0.0', 2121) #FTP一般使用21,20端口 
        server = FTPServer(address, handler) #FTP服务器实例 
        
        # set a limit for connections 
        server.max_cons = 256 
        server.max_cons_per_ip = 1  #一台pc只允许登录一个ftp客户端
        
        # 开启服务器 
        print("Start FTP serve Forever ...")
        server.serve_forever() 
    except Exception as e:
        print("Start Fail: {}".format(e))

    output, err = p1.communicate()    
    if output == None:
        output = "(NO OUTPUT. Please Redirect stdout&stderr)"
    print(":-------------------------:")
    print("PandoraCoordinator Output:",output)
    print(":-------------------------:")
    print("PandoraCoordinator Err:",err)
    print(":-------------------------:")

    output, err = p2.communicate()    
    if output == None:
        output = "(NO OUTPUT. Please Redirect stdout&stderr)"
    print(":-------------------------:")
    print("PandoraRenderHandler Output:",output)
    print(":-------------------------:")
    print("PandoraRenderHandler Err:",err)
    print(":-------------------------:")

if __name__ == '__main__':
    main()