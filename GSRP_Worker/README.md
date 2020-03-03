# 配置
1. 安装maya2019
1. 安装python3，pip， 以及模块psutil
1. 配置config.py中的IP前缀为当期局域网网段
1. 配置config.py中的Maya_path 和Mayapy_path 
        "Maya_path": "C:\\Autodesk\\Maya2019\\bin\\Render.exe",
		"Mayapy_path":"C:\\Autodesk\\Maya2019\bin\\mayapy.exe"
1. 复制copy_this_to_startup.bat 到 开机启动文件夹： C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
该地址在各个系统下可能有所不同。
【重要】：根据该路径修改copy_this_to_startup.bat中 cd 命令的路径，保证脚本可以找到GSRP_Server文件夹。
1. 根据该地址路径同时需要更新run_pandora_node.bat的代码。

```
cd ../../../../../
```

# 运行(如果通过copy_this_to_startup.bat运行， 跳过此步骤)
直接运行。在上一层目录 Pandora 下执行：
```
python ./GSRP_Worker/prerun.py
```
系统自启动运行。 如果bat提交本已经复制到startup路径下， 则重启将自动启动。

# 备注





