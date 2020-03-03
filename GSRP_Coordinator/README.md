
    
# 运行前准备
+ 服务器安装python3;
+ 服务器打开smb服务
+ 服务器配置开启文件共享访问无需验证  https://blog.csdn.net/RBPicsdn/article/details/79615991
+ 在D盘创建文件夹GSRP_Server，并设置为共享目录
+ 服务器共享目录中共享账户加入Guest用户
+ 从代码仓库拷贝 python27.zip、Pandora、GSRP_Worker、GSRP_Submitter、GSRP_Coordinator、GSRP_NodeProxy文件夹到文件夹GSRP_Server
+ 其中的GSRP_Coordinator\Scripts\PandoraCoordinator\PandoraCoordinator.py同 Pandora/Scripts/PandoraCoordinator下的文件保持一致;

# 运行调度中心Coordinator
在 GSRP_Coordinator 的同级目录下（即 D:\GSRP_Server），运行：
```
python GSRP_Coordinator/run.py
```
或者直接双击运行run.bat


在配置界面中， 配置Pandora Root为GSRP_Coordinator文件夹的路径。 例如： 
```
D:\\GSRP_Server\\GSRP_Coordinator
```

在配置界面中， 配置rootPath为GSRP_Coordinator文件夹的路径。 例如： 
```
C:\Users\XXXX\Documents\PandoraRepository
```
如何查看XXXX是什么，可以直接点进计算机的文档文件夹的路径，则可以看出用户名


# 默认路径，便于查看Pandora.json里面的配置，暂时还不知道要看哪些内容
+ 全局配置文件Pandora.json默认创建路径, 该路径自动创建，无需更改。：
    ```
    C:\Users\XXXX\Documents\Pandora\Pandora.json
    ```