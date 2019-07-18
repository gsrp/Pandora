import os, sys, shutil, zipfile, time


if len(sys.argv) == 2:
    fast = sys.argv[1]
else:
    fast = ""

def Unzip(src, dest):
    shutil.unpack_archive(src, dest)

def Zip(src, dest, format): 
    if not os.path.isdir(src):
        print("archive path need folder type ")
        return
    shutil.make_archive(dest, format, src)


if not os.path.exists("./GSRP_Code"):
    os.mkdir("./GSRP_Code")

p3 = "./GSRP_Code/Pandora"
if os.path.exists(p3):
    shutil.rmtree(p3)

if fast == "fast":
    shutil.copytree("./Pandora/Plugins",p3+'/Plugins',ignore=shutil.ignore_patterns('*.pyc'))
    shutil.copytree("./Pandora/Scripts",p3+"/Scripts",ignore=shutil.ignore_patterns('*.pyc'))
else:
    shutil.copytree("./Pandora",p3,ignore=shutil.ignore_patterns('*.pyc'))
print("Copy {} Ok!".format(p3))

shutil.copy2(p3+"/Scripts/PandoraCoordinator.py", "./GSRP_Coordinator/Scripts/PandoraCoordinator/")

p1 = "./GSRP_Code/GSRP_Coordinator"
if os.path.exists(p1):
    shutil.rmtree(p1)
if not os.path.exists(p1+"/Scripts/PandoraCoordinator/"):
    os.makedirs(p1+"/Scripts/PandoraCoordinator/")

shutil.copy2("./GSRP_Coordinator/Scripts/PandoraCoordinator/PandoraCoordinator.py",p1+"/Scripts/PandoraCoordinator/")
shutil.copy2("./GSRP_Coordinator/README.md",p1)
shutil.copy2("./GSRP_Coordinator/requirements.txt",p1)
shutil.copy2("./GSRP_Coordinator/run.py",p1)
# shutil.copytree("./GSRP_Coordinator/",p1,ignore=shutil.ignore_patterns('*.pyc'))
print("Copy {} Ok!".format(p1))

p2 = "./GSRP_Code/GSRP_Worker"
if os.path.exists(p2):
    shutil.rmtree(p2)
shutil.copytree("./GSRP_Worker",p2)
print("Copy {} Ok!".format(p2))

p4 = "./GSRP_Code/python27.zip"
if os.path.exists(p4):
    os.remove(p4)
if fast == "fast":
    pass
else:
    shutil.copy2("./python27.zip","./GSRP_Code/")

print("Copy {} Ok!".format(p4))


ver = time.strftime("%Y%m%d.%H.%M.%S",time.localtime(time.time()))
print("Zip {} To {} ...".format(os.path.join(os.path.dirname(__file__),"GSRP_Code"),"GSRP_Code_"+ver+".zip"))
Zip(os.path.abspath("./GSRP_Code"),os.path.join(os.path.abspath(".\\"),"GSRP_Code_"+ver), 'zip')

shutil.rmtree("./GSRP_Code")