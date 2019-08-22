# -*- coding: utf-8 -*-

import platform,sys,pprint,os
import socket,time,psutil

pp = pprint.PrettyPrinter(indent=4)

#多网卡情况下，根据前缀获取本地IP
def wait(rendercmdPath, timeoutMinitues):
    try:
        fp = open(rendercmdPath,'r')
        rendercmd = fp.read()
        fp.close()
    except Exception as e:
        print("[wait.py] Fail To Open File: {}".format(e))
        return

    tick = 0
    exsist = False
    # 首先检查是否存在maya进程，如果不存在，则不需要等待
    for pid in psutil.pids():
        try:
            p = psutil.Process(pid)  
            cmd = p.cmdline() # example: ['C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python37\\python.exe', '.\\run.py']
        except:
            continue
        if rendercmd == ' '.join(cmd):
            exsist = True
            break
    if not exsist:
        print("Not Maya Render Is Running, No Need To Wait...")
        return
    
    print("[wait.py] Not Maya Render Is Running, Wait...")
    # 存在maya进程， 进行等待
    while 1:
        if tick >= timeoutMinitues * 60:
            print("Working Timeout...   > {} min.".format(tick/60))
            return
        finish = True
        for pid in psutil.pids():
            try:
                p = psutil.Process(pid)
                cmd = p.cmdline()
            except:
                continue
            # 找到进程， 说明还在运行
            if rendercmd == ' '.join(cmd):
                finish = False
                break
        # 遍历完所有的进程， 没有匹配到maya进程
        if finish:
            print("Working Finish ...  Elapsed {} min.".format(tick/60))
            return
        time.sleep(5)
        tick = tick+5 
        if tick % 60 == 0:
            print("Working Elapsed: {} min.".format(tick/60))
            print("            Cmd: {}\n".format(rendercmd))

def main():
    if len(sys.argv[1]) == 1:
        print("Please Specify RenderCmd File Path!")
        return
    rendercmd_path = sys.argv[1]
    print("Wait_For_Render.py] rendercmd_path: {}".format(rendercmd_path))
    wait(rendercmd_path,120)

    return
    
if __name__ == '__main__':
    main()