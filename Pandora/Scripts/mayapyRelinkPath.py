# -*- coding: utf-8 -*-
import os,sys
try:          
    import maya.standalone     
except:          
    pass
import maya.cmds as cmds

def openScene(path = None):
    if os.path.exists(path):
        try:
            opend = cmds.file(path, o = True, f = True, esn = True)
            print("\n\n[MayaWorker] Opend Sence: {}\n\n".format(opend))
        except:
            print("[MayaWorker] Opend Sence:ERRRRRRRRRRRRRRR")
        return opend

def save(): 
    # check if there are unsaved changes
    fileCheckState = cmds.file(q=True, modified=True)
    print("Save Scene ... ",fileCheckState)
    # if there are, save them first ... then we can proceed 
    if fileCheckState:
        print("Save Scene ... ")
        cmds.SaveScene()

def saveWorkingScene(np):

    newpath = np.replace("\\","/")
    outLength = len(newpath)
    print("Save Scene ... newpath: ",newpath)
    if outLength > 260:
        print("[MayaWorker] The newpath is longer than 260 characters (%s), which is not supported on Windows." % outLength)
        return False

    cmds.file(rename=newpath)
    try:
        cmds.file(save=True)
    except Exception as e:
        print("Save Scene ... Fail: ",e)
        return False

    if not os.path.exists(newpath):
        return False

    return newpath

      
def relink(path):
    results = []
    openScene(path)
    print("openScene OK: ", path)
    links = cmds.filePathEditor(query=True, listDirectories="") 
    if links == None:
        return
    print("filePathEditor OK: ", links)
    for link in links: 
        pairs =  cmds.filePathEditor(query=True, listFiles=link, withAttribute=True, status=True)    
        print("pairs: ", pairs)        
        l = len(pairs)
        items = l/3
        order = {}
        index = 0
        
        for i in range(0,items):
            order[pairs[index+1]] = [pairs[index],pairs[index+2]]
            index = index + 3  
                        
        for key in order:            
            if order[key][1] == "0": 
                if repath(key, order[key][0], path):
                    results.append(key)   
    # save()
    saveWorkingScene(path)
    print("[MayaWorker] After Relink:{}".format(cmds.filePathEditor(query=True, listDirectories="")))

def repath(node, file, project_path):
	matches = []
	for root, dirnames, filenames in os.walk(os.path.dirname(project_path)):
		for x in filenames:
			if x == file:
				matches.append([root,os.path.join(root, x)]) 
			elif x.split(".")[0] == file.split(".")[0]: 
				x_ext = x.split(".")[len(x.split("."))-1]
				file_ext = file.split(".")[len(file.split("."))-1]
				if x_ext == file_ext:
					matches.append([root,os.path.join(root, x)])
				
	if len(matches)>0:   
		return cmds.filePathEditor(node, repath=matches[0][0])      
	
	return None 
    
if __name__ == "__main__":
    try:
        maya.standalone.initialize('python')
    except:
        print("[MayaWorker] standalone already running")
    print("[MayaWorker] Initialize OK.")
    
    if os.path.exists(sys.argv[1]):
        relink(sys.argv[1])
    else:
        print("@@@@ No Such File:     %s" % sys.argv[1])
    
    if float(cmds.about(v=True)) >= 2016.0:
        maya.standalone.uninitialize()
        print("[MayaWorker] Uninitialize OK.")
