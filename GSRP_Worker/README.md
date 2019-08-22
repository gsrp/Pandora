# 配置
1. 配置config.py中的IP前缀为当期局域网网段
1. 根据安装的maya版本修改 \Documents\Pandora\Pandora.json  :  Maya_override=true   Maya_path="C:\\Autodesk\\Maya2019\\bin\\Render.exe"   Mayapy_path="C:\\Autodesk\\Maya2019\\bin\\mayapy.exe"  
1. 复制run_pandora_node.vbs, run_pandora_node.bat 到 开机启动文件夹： C:\Users\Administrator\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
该地址在哥哥系统下可能有所不同， 根据该地址路径同时需要更新run_pandora_node.bat的代码。

```
    "dccoverrides": {
        "Houdini_path": "", 
        "3dsMax_path": "", 
        "Maya_override": false, 
        "Blender_path": "blender.exe", 
        "Blender_override": false, 
        "Maya_path": "C:\\Autodesk\\Maya2019\\bin\\Render.exe", 
        "Houdini_override": false, 
        "3dsMax_override": false
    }
```

# 运行
在上一层目录 Pandora 下执行：
```
python ./GSRP_Worker/prerun.py
```

# 备注





