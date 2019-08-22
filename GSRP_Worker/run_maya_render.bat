@echo off
setlocal enabledelayedexpansion

set work_path="C:\\GSRP_Server\\GSRP_Worker"
set gongzuo_pan=!work_path:~0,2!
@echo [INIT] work_path  = %work_path%

set dangqian_pan=%~d0 
set dangqian_lujing=%cd%

:: 空闲时定时检查是否有渲染任务
:tryFetch
cd %dangqian_pan%
cd %dangqian_lujing%
set wait=10
@echo ++++
@echo [STEP 0] Try Maya Reander . Wait %wait% s ...
@echo ++++
:: 等待10s 
ping -n %wait% 127.0.0.1>nul
:: 尝试下载文件
call :checkAndRun 

:checkAndRun
for  /f "delims=" %%c in ('dir /ad/b/s "%work_path%"') do (
    @echo ###########################
    @echo [run.bat] Get Maya File Path : %%c
    @echo ###########################
    call :execcmd 

    @echo Wait 3s to start wait work over....
    ping -n 3 127.0.0.1>nul
    goto waitWork
)

:: 执行文本中的命令     
:execcmd
for  /f "delims=" %%c in ('dir /ad/b/s "%work_path%"') do (
    @echo ###########################
    @echo [run.bat] Start Render. CmdFile: %%c\rendercmd.txt
    @echo ###########################
    for /f "delims=" %%i in (%%c\rendercmd.txt) do (
        @echo EXEC Cmd:  %%i
        start %%i
    )
    goto:eof
)

:: 等待任务完成
:waitWork
for  /f "delims=" %%c in ('dir /ad/b/s "%work_path%"') do (
    @echo ###########################
    @echo Wait work to finish ...
    @echo ###########################
    cd %gongzuo_pan%
    cd %work_path%

    python .\Wait_For_Render.py %%c\rendercmd.txt
    ping -n 3 127.0.0.1>nul
    del %%c\rendercmd.txt
    :: 继续领任务 
    goto tryFetch 
)
