# IPython log file

get_ipython().magic('startlog D:\\myproject\\pyhook\\tmp_code.py')
get_ipython().magic('logstart D:\\myproject\\pyhook\\tmp_code.py')
import PyHook3
import pythoncom
import win32api
from colorama import Fore

def abortkey(event):
    if(event.Key)=='F12':
        win32api.PostQuitMessage()
    return True

def mouseup(event):
    global start_x,start_y
    start_x,start_y=event.Position
    print(Fore.GREEN+'{1}'.format(event.Position)+Fore.RESET)
    return True

def mousedown(event):
    global end_x,end_y
    enx_x,end_y=event.Position
    print(Fore.RED+'{1}'.format(event.Position)+Fore.RESET)
    return True

def main():  
  # 创建一个“钩子”管理对象  
  hm = PyHook3.HookManager()  
  # 监听所有键盘事件  
  hm.KeyDown = abortkey  
  # 设置键盘“钩子”  
  hm.HookKeyboard()  
  # 监听所有鼠标事件  
  hm.MouseLeftDown = mouseup
  hm.MouseLeftUp = mousedown
  # 设置鼠标“钩子”  
  hm.HookMouse()  
  # 进入循环，如不手动关闭，程序将一直处于监听状态  
  pythoncom.PumpMessages() 
  
main()
