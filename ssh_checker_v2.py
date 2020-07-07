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
line_bot_api = LineBotApi('YOUR_LineBot_Channel access token')
to = "YOUR ROOM ID" # Room
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