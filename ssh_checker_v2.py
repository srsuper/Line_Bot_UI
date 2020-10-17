import os
import requests
from linebot import LineBotApi, WebhookHandler
from linebot.models import *
import json
import datetime
from time import sleep
import time
import os
import random
import win32gui

def winEnumHandler(hwnd,ctx):
    if win32gui.IsWindowVisible(hwnd):
        windows_list.append(win32gui.GetWindowText(hwnd))

pyPath = os.path.dirname(os.path.abspath(__file__))
line_bot_api = LineBotApi('3ckCQeHp+WMyT1LYRkdApHoRucfJJiufV/lvr2qWnODDrx8FGcGF9HcjbA4ZlySWXn7/bvTx+0IGoCTYMzecGXGMLuTGoy1Qf2ZFr0RclVLEoyNZcuEjqGRxesPDQQwXEPKU1q2JTMSzfuo3JZIN+wdB04t89/1O/w1cDnyilFU=')
to = "1654167585" # Room
while True:
    windows_list =[]
    win32gui.EnumWindows(winEnumHandler, None)
    # print(windows_list)
    matching = [s for s in windows_list if "OpenSSH SSH client" in s]
    # print(matching)
    if len(matching) == 0:
        # print("Serveo disconnected")
        os.system("C:\\Users\\SP3back\\Desktop\\Start_serveo.bat")
        print("Serveo re-connecting " + datetime.datetime.now().strftime("%m/%d %H:%M:%S"))
        # print()
        sleep(60)
    else:
        # print("Serveo connecting")
        sleep(5)