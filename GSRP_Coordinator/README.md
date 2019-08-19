# 默认路径
+ 全局配置文件Pandora.json默认创建路径为：
    ```
    C:\Users\XXXX\Documents\Pandora\Pandora.json
    ```
    该路径自动创建，无需更改。

# 运行前准备
+ 服务器打开smb服务
+ 服务器配置开启文件共享访问无需验证  https://blog.csdn.net/RBPicsdn/article/details/79615991
+ 在D盘创建文件夹GSRP_Server，并设置为共享目录
+ 服务器共享目录中共享账户加入Guest用户
+ 从代码仓库拷贝 Pandora、GSRP_Worker、GSRP_Submitter、GSRP_Coordinator文件夹 ( 其中的PandoraCoordinator.py同 Pandora/Scripts下的文件保持一致 )，到文件夹GSRP_Server

# 运行调度中心Coordinator
在 GSRP_Coordinator 的同级目录下，运行：
```
python GSRP_Coordinator/run.py
```
在配置界面中， 配置rootPath为GSRP_Coordinator文件夹的路径。 例如： 
```
D:\\GSRP_Server\\GSRP_Coordinator
```


