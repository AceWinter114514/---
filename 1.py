import numpy as np
import pyautogui as pag
import pygetwindow as gw
import pytesseract
from PIL import Image
import re
import time
import cv2

custom_config = r'--oem 3 --psm 7 outputbase digits'
#改为你安装tesseract的路径。
pytesseract.pytesseract.tesseract_cmd = r'E:\Program Files\Tesseract-OCR\tesseract.exe'

w = 0
dtq = []


"""如下number_0~9都是画数字的函数，如果不符合你的需求可以更改"""
def number_0(start_x, start_y):
    pag.moveTo(start_x, start_y)
    pag.mouseDown()
    pag.moveRel(20, 0)
    pag.moveRel(0, 20)
    pag.moveRel(-20, 0)
    pag.moveRel(0, -20)
    pag.mouseUp()

def number_1(start_x, start_y):
    pag.moveTo(start_x, start_y - 25)
    pag.mouseDown()
    pag.moveRel(0, 50)
    pag.mouseUp()

def number_2(start_x, start_y):
    pag.moveTo(start_x, start_y)
    pag.mouseDown()
    pag.moveRel(30, 0)
    pag.moveRel(-30, 30)
    pag.moveRel(30, 0)
    pag.mouseUp()

def number_3(start_x, start_y):
    pag.moveTo(start_x, start_y)
    pag.mouseDown()
    pag.moveRel(30, 0)
    pag.moveRel(0, 20)
    pag.moveRel(-30, 0)
    #pag.mouseUp()
    pag.moveTo(start_x + 20, start_y + 20)
    #pag.mouseDown()
    pag.moveRel(0, 20)
    pag.moveRel(-30, 0)
    pag.mouseUp()

def number_4(start_x, start_y):
    pag.moveTo(start_x, start_y)
    pag.mouseDown()
    pag.moveRel(-20, 20)
    pag.moveRel(55, 0)
    pag.mouseUp()
    pag.moveTo(start_x + 10, start_y)
    pag.mouseDown()
    pag.moveRel(0, 69)
    pag.moveRel(0, 1)
    pag.mouseUp()

def number_5(start_x, start_y):
    pag.moveTo(start_x, start_y)
    pag.mouseDown()
    pag.moveRel(0, 20)
    pag.moveRel(20, 0)
    pag.moveRel(0, 20)
    pag.moveRel(-20, 0)
    pag.mouseUp()
    pag.moveTo(start_x, start_y)
    pag.mouseDown()
    pag.moveRel(23, 0)
    pag.mouseUp()

def number_6(start_x, start_y):
    pag.moveTo(start_x, start_y)
    pag.mouseDown()
    pag.moveRel(0, 35)
    pag.moveRel(20, 0)
    pag.moveRel(0, -20)
    pag.moveRel(-20, 0)
    time.sleep(0.08)
    pag.mouseUp()

def number_7(start_x, start_y):
    pag.moveTo(start_x, start_y)
    pag.mouseDown()
    pag.moveRel(20, 0)
    pag.moveRel(0, 90)
    pag.mouseUp()

def number_8(start_x, start_y):
    pag.moveTo(start_x, start_y)
    pag.mouseDown()
    pag.moveRel(20,0)
    pag.moveRel(-20, 40)
    pag.moveRel(20, 0)
    pag.moveRel(-20, -40)
    pag.mouseUp()

def number_9(start_x, start_y):
    pag.moveTo(start_x, start_y)
    pag.mouseDown()
    pag.moveRel(20, 0)
    pag.moveRel(0, 20)
    pag.moveRel(-20, 0)
    pag.moveRel(0, -20)
    pag.mouseUp()
    pag.moveTo(start_x + 20, start_y)
    pag.mouseDown()
    pag.moveRel(0, 120)
    pag.mouseUp()

def bigger(start_x, start_y):
    pag.moveTo(start_x, start_y)
    pag.mouseDown()
    pag.moveRel(10, 10)
    pag.moveRel(-10, 10)
    pag.mouseUp()
def smaller(start_x, start_y):
    pag.moveTo(start_x, start_y)
    pag.mouseDown()
    pag.moveRel(-10, 10)
    pag.moveRel(10, 10)
    pag.mouseUp()
#cws函数为让你的scripy窗口显示在显示屏上
def cws(window_title):
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        if window and not window.isMinimized:
            window.activate()
            return window
    except IndexError as e:
        print(e)
#四则运算
def oac(region):
    global w
    try:
        i1 = 0
        screenshot = pag.screenshot(region=region)
        #图片保存，不建议启动除非是调试，因为会显著减慢运行速度
        #screenshot.save("awa.png")
        '''图片二值化，不建议在这里开启，可能会检测失败'''
        #gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(screenshot)
        text = text.replace(' ?', '').replace('?', '').replace('=', '').replace('| ', '').replace('|', '').replace('x', '*').replace('÷','/')
        print("算式:", text)
        pt = r'(\d+)\s*([\+\-\*\/])\s*(\d+)'
        match = re.match(pt, text)
        if match:
            w = 0
            result = eval(text)
            for i in str(result):
                i1 += 1
                start_x = dtq[0] - 21 * len(str(result)) + 50 * (i1 - 1)
                start_y = dtq[1]
                eval(f"number_{i}(start_x, start_y)")
                #time.sleep(1)
            #pag.mouseUp()
            return result
        if not match:
            return "不符合正则表达式"
        else:
            print("没有题目")
            return None
    except Exception as e:
        print(f"OCR识别或计算失败: {e}（纳尼，程序比不过小朋友？）")
        return None
#比大小
def oacsb(region1,region2):
    try:
        i1 = 0
        screenshot = pag.screenshot(region=region1)
        screenshot1 = pag.screenshot(region=region2)
        '''如下注释掉的时保存截图图片的代码，awa1.png为符号左边，awa2.png为符号右边，如果要保存的话会减慢运行速度'''
        #screenshot.save("awa1.png")
        #screenshot1.save('awa2.png')
        #此处将图片二值化以便检测数字，可以关掉，但容易检测不准。
        gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
        gray1 = cv2.cvtColor(np.array(screenshot1), cv2.COLOR_BGR2GRAY)
        text1 = pytesseract.image_to_string(gray, config=custom_config)
        text2 = pytesseract.image_to_string(gray1, config=custom_config)
        number1a = re.findall(r'\d+', text1)
        number2a = re.findall(r'\d+', text2)
        number1 = ''.join(number1a)
        number2 = ''.join(number2a)
        if number1 == '':
            print("未识别到第一个区域的数字")
            return None
        if number2 == '':
            print("未识别到第二个区域的数字")
            return None
        if int(number1) > int(number2):
            start_x = dtq[0]
            start_y = dtq[1]
            eval("bigger(start_x, start_y)")
            return number1,number2
        elif int(number1) < int(number2):
            start_x = dtq[0]
            start_y = dtq[1]
            eval("smaller(start_x, start_y)")
            return number1,number2
        else:
            return '不符合正则表达式'
    except IndexError as e:
        print(f"OCR识别或计算失败: {e}（纳尼，程序比不过小朋友？）")
        return None
def ql():
    try:
        p = pag.locateOnScreen('image1.png', confidence=0.7,grayscale=True)
        p1 = pag.locateCenterOnScreen('image.png', confidence=0.7,grayscale=True)
        if p and p1:
            dtq.clear()
            dtq.append(p1.x)
            dtq.append(p1.y)
            region = [int(p.left) - 230, int(p.top), 230 + w, int(p.height)]
            print(oac(region))
        else:
            print("还没有开始啊")
    except Exception as e:
        print(f"还没有开始啊{e}")
def ql2():
    try:
        p = pag.locateOnScreen('image2.png', confidence=0.7,grayscale=True)
        p1 = pag.locateCenterOnScreen('image.png', confidence=0.7,grayscale=True)
        if p and p1:
            dtq.clear()
            dtq.append(p1.x)
            dtq.append(p1.y)
            region1 = [int(p.left) - 120, int(p.top), 160 + w, int(p.height) + 10]
            region2 = [int(p.left) + 90, int(p.top), 150 + w, int(p.height) + 10]
            print(oacsb(region1, region2))
        else:
            print("还没有开始啊")
    except Exception as e:
        print(f"还没有开始啊{e}")
#windows_title用scripy显示手机显示屏的窗口名称定义。
window_title = "ONEPLUS A6013"
window = cws(window_title)

def main():
    if window:
        while True:
            '''不推荐两个都开启，因为我没逝过，总之就是你要炸哪里的鱼就开哪个'''
            #ql函数为四则运算
            ql()
            #ql2函数为比大小
            #ql2()
            #time.sleep(1)

if __name__ == "__main__":
    main()
