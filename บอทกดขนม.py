import webbrowser
import pyautogui
import time
import requests
import threading

import keyboard
import tkinter as tk
import tkinter.messagebox
from tkinter import scrolledtext

cancelByKeyboard = False

def automateURL(url, num):
    webbrowser.open(url)
    time.sleep(6)

    retry = 2
    try:
        position = pyautogui.locateOnScreen("basket.png", grayscale=False, confidence=0.9)
        if position:
            x, y = pyautogui.center(position)
            pyautogui.click(x, y)
            pyautogui.moveTo(x+100, y+100)
            time.sleep(3)
            for i in range(1, num):
                if (keyboard.is_pressed('Ctrl+C')):
                    global cancelByKeyboard
                    cancelByKeyboard = True
                    break
                position = pyautogui.locateOnScreen("add.png", grayscale=False, confidence=0.7)
                if(position):
                    x, y = pyautogui.center(position)
                    pyautogui.click(x, y)
                    pyautogui.moveTo(x+100, y+100)
                    retry = 2
                    if(pyautogui.locateOnScreen("notenougth.png", grayscale=False, confidence=0.7)):
                        result_text.insert(tk.END, "ของหมดคลัง แล้ว ได้แค่ " + str(i+1) + " จาก " + str(num) + " ชิ้น\n")
                        result_text.update()
                        pyautogui.keyDown('ctrl')
                        pyautogui.keyDown('w')
                        pyautogui.keyUp('ctrl')
                        pyautogui.keyUp('w')
                        return i+1
                    time.sleep(1.5)
                else:
                    if(retry > 0):
                        retry -= 1
                        i+=1
                        continue
                    else:
                        print("Image + not found on the screen.")
                        pyautogui.keyDown('ctrl')
                        pyautogui.keyDown('w')
                        pyautogui.keyUp('ctrl')
                        pyautogui.keyUp('w')
                        return 0

        else:
            print("Image + not found on the screen.")
            pyautogui.keyDown('ctrl')
            pyautogui.keyDown('w')
            pyautogui.keyUp('ctrl')
            pyautogui.keyUp('w')
            return 0
    except:
        result_text.insert(tk.END, "Have Some Error!!\n")
        result_text.update()
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('w')
        pyautogui.keyUp('ctrl')
        pyautogui.keyUp('w')
        return 0

    # print(pyautogui.getActiveWindow())
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('w')
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('w')
    return num

def updateSheet(countNumList):
    api_url = "https://script.google.com/macros/s/AKfycbxepS5r52QOsqUPSzkfsxgaBc06zaE71MFZoo5FQPrf8sJxAumVs0s5vBmsqNKlecM/exec?data="
    api_url+=str(countNumList)
    requests.get(api_url)
    root.after(1000, show_complete_window)

        

def runTask():
    countNumList = []
    api_url = "https://script.google.com/macros/s/AKfycbwoh6p28yXjD2pFoWJQxkp1rwowrU3RseQJYjGfO6cuWeCLZHINUhORgH2pXFO622rS6w/exec"
    response = requests.get(api_url)
    if response.status_code == 200:
        jsonData = response.json()
        jsonList = jsonData['data']

        numNow = 1
        allLen = len(jsonList)
        for dataBlock in jsonList:
            basketNum = automateURL(dataBlock['url'], dataBlock['count'])
            if(basketNum>0):
                result_text.insert(tk.END, "ยัดของลงตะกร้าสำเร็จ URL หมายเลข" + str(numNow) + " จาก " + str(allLen) + "\n")
                result_text.insert(tk.END, "----------------------------------\n")
                result_text.update()
            else:
                result_text.insert(tk.END, "ยัดของลงตะกร้าผิดพลาด URL หมายเลข" + str(numNow) + " จาก " + str(allLen) + "\n")
                result_text.insert(tk.END, "----------------------------------\n")
                result_text.update()
            countNumList.append(basketNum)
            numNow+=1
            if(cancelByKeyboard):
                result_text.insert(tk.END, "ยกเลิกกระบวนการสำเร็จ!!!\n")
                return
    
        webbrowser.open("https://www.makro.pro/")
        time.sleep(5)
        if pyautogui.locateOnScreen("openbasket.png", grayscale=False, confidence=0.6):
            x, y = pyautogui.center(pyautogui.locateOnScreen("openbasket.png", grayscale=False, confidence=0.6))
            pyautogui.click(x, y)
            time.sleep(2)
        updateSheet(countNumList)
    
    else:
        result_text.insert(tk.END, "API เสีย เริ่มงานไม่ได้ครับ\nAPI failed with status code: " + str(response.status_code))
        result_text.update()
        root.after(1000, show_fail_window)

# GUI Zone
def letgo():
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "เริ่มการดำเนินการ: \n")
    result_text.update()
    
    thread = threading.Thread(target=runTask())
    thread.start()
        

def show_complete_window():
    tk.messagebox.showinfo("Complete", "เรียบร้อยครับ!!")

def show_fail_window():
    tk.messagebox.showinfo("Complete", "เรียบร้อยครับ หมายถึงมันระเบิด!!")

root = tk.Tk()
root.title("บอทกดขนม")
instructions = """คำเตือนก่อนการใช้งาน:
    เมาส์และหน้าจอของคุณจะถูกยืมใช้งานชั่วคราว ระหว่างประมวลผลสามารถไปหาอะไรกินหรือทำอย่างอื่นรอก็ได้
---------------------------------------------------------------------------------------------------------------------------------------------
สิ่งที่ต้องทำก่อนกดปุ่มเริ่ม:
    1. ปิดหน้าต่างทุกชนิดยกเว้น Google Chrome ที่เปิดไว้เต็มจอ และไว้ที่จอข้างซ้าย
    2. เอาหน้าต่างบอทนี้ไว้ที่หน้าจอฝั่งขวา
    3. Google Chrome เปิด Tab เว็บ https://www.makro.pro/ ไว้เท่านั้น และทำรายการต่อไปนี้ให้หมด
        3.1. ล็อกอิน User พร้อมเพิ่มของเข้าตะกร้า
        3.2. ในตะกร้าต้องไม่มีของอยู่สักชิ้นเดียว
        3.3. ยืนยันตำแหน่งที่ต้องการและยืนยันคุกกี้ให้พร้อม

**คำเตือน : ระบบนี้เป็นระบบเพิ่มของเข้าตะกร้าอัตโนมัติ ไม่รวมการกดจ่ายแต่อย่างใด เมื่อเกิดปัญหาขึ้นและต้องการหยุดโปรแกรมให้พิมพ์คีย์บอร์ด Ctrl+C ค้างไว้**
"""

# Text box to display instructions
instructions_font = ("Helvetica", 12)
instructions_label = tk.Label(root, text=instructions, font=instructions_font, wraplength=800, justify=tk.LEFT)
instructions_label.pack(padx=10, pady=10)

# Button Run the function
run_button = tk.Button(root, text="Run", command=letgo)
run_button.pack()

# Create Text box to display results
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
result_text.pack(padx=10, pady=10)

root.mainloop()