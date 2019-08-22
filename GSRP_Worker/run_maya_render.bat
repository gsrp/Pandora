@echo off
setlocal enabledelayedexpansion

set work_path=C:\GSRP_Server\GSRP_Worker
set gongzuo_pan=!work_path:~0,2!
@echo [INIT] work_path  = %work_path%

set dangqian_pan=%~d0 
set dangqian_lujing=%cd%
@echo [INIT] dangqian_pan  = %dangqian_pan%
@echo [INIT] dangqian_lujing  = %dangqian_lujing%

:: 空闲时定时检查是否有渲染任务
:tryFetch
set wait=10
@echo ++++
@echo [STEP 0 tryFetch] Try Maya Reander . Wait %wait% s ...
@echo ++++
:: 等待10s 
ping -n %wait% 127.0.0.1>nul
:: 尝试下载文件
call :checkAndRun 

:checkAndRun
@echo [STEP 1 checkAndRun] Get Maya File Path : %work_path%
call :execcmd 
ping -n 3 127.0.0.1>nul
goto waitWork


:: 执行文本中的命令     
:execcmd
if exist %work_path%\rendercmd.txt (
	@echo ###########################
	@echo [STEP 2 execcmd] Start Render. CmdFile: %work_path%\rendercmd.txt
	@echo ###########################
	for /f "delims=" %%i in (%work_path%\rendercmd.txt) do (
		@echo EXEC Cmd:  %%i
		start %%i
	)
) else (
	@echo [STEP 2.1 execcmd] Not Exsist CmdFile: %work_path%\rendercmd.txt
)
goto:eof


:: 等待任务完成
:waitWork

if not exist %work_path%\rendercmd.txt (
	@echo [STEP 3.1 waitWork] Not Exsist CmdFile: %work_path%\rendercmd.txt
	goto tryFetch
)
@echo ###########################
@echo [STEP 3 waitWork] Wait work to finish ...
@echo ###########################
python C:\GSRP_Server\Pandora\Plugins\Apps\Maya\Scripts\Wait_For_Render.py %work_path%\rendercmd.txt

@echo [STEP 3 waitWork] Render Finished

ping -n 3 127.0.0.1>nul
del %work_path%\rendercmd.txt
:: 继续领任务 
goto tryFetch
