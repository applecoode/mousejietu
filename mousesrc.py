import PyHook3
import pythoncom
import win32api
from colorama import Fore
from PIL import Image, ImageGrab
from common import ocr,methods
import configparser
config = configparser.ConfigParser()
config.read('./config/configure.conf', encoding='utf-8')

ctrlflag=0

def abortkey(event):
    global ctrlflag,hm
    if event.Key=='F12':
        hm.UnhookKeyboard()
        hm.UnhookMouse()
        hm=None
        win32api.PostQuitMessage()
    # if event.Key=='Lcontrol' and event.MessageName=='key down':
    if event.Key=='A':
        print(Fore.GREEN+'请用鼠标框选你的题目和答案:'+Fore.GREEN)
        ctrlflag=1
    # if event.Key=='Lcontrol' and event.MessageName=='key up':
    return True

def mouseup(event):
    global start_x,start_y,ctrlflag
    if ctrlflag==1:
        start_x,start_y=event.Position
        print(Fore.GREEN+str(start_x)+','+str(start_y)+Fore.RESET)
        return True
    else:
        print('未激活截图模式!')
        return True

def mousedown(event):
    global end_x,end_y,ctrlflag
    if ctrlflag==1:
        end_x,end_y=event.Position
        print(Fore.RED+str(end_x)+','+str(end_y)+Fore.RESET)
        if start_x<end_x and start_y<end_y:
            image = ImageGrab.grab((start_x, start_y, end_x, end_y))
            image.save('./screenshot.png',format='PNG')
            # image = Image.open("../screenshot.png")
            question, choices = ocr.ocr_img_baidu(image,config)
            print(choices)
            methods.run_algorithm(2,question,choices)
            ctrlflag=0
        else:
            print(Fore.RED+'请换一种姿势重新选择'+Fore.RESET)
            ctrlflag=0
        return True
    else:
        print('未激活截图模式!')
        return True

def main():
    print(Fore.RED+"""
    使用方法:\n
    1.像正常答题一样打开程序或浏览器\n
    2.为了便于查看搜索结果,建议适当调整窗口使浏览器和该窗口都能显示\n
    3.开始答题,按键盘上的A激活截图模式\n
    4.按住鼠标左键框选题目和选项,松开左键完成截图\n
    5.等待搜索结果,建议选择绿色数字最大的选项\n
    6.按F12退出该程序"""
    +Fore.RESET)
    global hm
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
    
    
if __name__ == '__main__':
    main()