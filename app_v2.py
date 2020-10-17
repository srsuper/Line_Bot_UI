from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import configparser
import requests
import random
from linebot.models.send_messages import StickerSendMessage
from googletrans import Translator
from gtts import gTTS
from time import sleep
import time
import json
import datetime
import re
from pytube import YouTube
pyPath = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
line_bot_api = LineBotApi('3ckCQeHp+WMyT1LYRkdApHoRucfJJiufV/lvr2qWnODDrx8FGcGF9HcjbA4ZlySWXn7/bvTx+0IGoCTYMzecGXGMLuTGoy1Qf2ZFr0RclVLEoyNZcuEjqGRxesPDQQwXEPKU1q2JTMSzfuo3JZIN+wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('dc3e513abb672e4764348401d67af1ac')

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Reply功能
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    r_source = json.loads(str(event.source))
    try: # weather verify userID, roomID, groupID
        chat_fromID = str(r_source['groupId'])
        chat_userID = str(r_source['userId'])
    except:
        try:
            chat_fromID = str(r_source['roomId'])
            chat_userID = str(r_source['userId'])
        except:
            chat_fromID = str(r_source['userId'])
            chat_userID = str(r_source['userId'])
    target = 0
    num = 0
    chat_text = event.message.text
    chat_time = event.timestamp
    key = event.message.text
    LanguageList = ["中文","zh-tw","英文","en","日文","ja","韓文","ko","簡中","zh-cn","繁中","zh-tw","菲文","tl"] 
    if  key[0:28] == "https://www.instagram.com/p/":
        key = key
    elif key[0:30] == "https://instagram.com/stories/":
        key = key
    elif key[key.find('http'):key.find('http')+21] == "https://v.douyin.com/":
        key = key[key.find('http'):key.find("/",key.find('http')+21)+1]
    elif key[0:25] == "https://www.facebook.com/":
        key = key
    elif key.find("youtu") != -1:
        key = key
        # print(key)
    elif key.find('moptt') != -1:
        key = key[key.find('https'):]
    else:
        key = str.upper(key)  
    if  (key[0:1] == "#") and key[1:] != "":
        if  key.find(" ") != -1:
            try:
                num = int(key[key.find(" ")+1:])
                target = key[1:key.find(" ")]
                key = key[0:1]
            except: 
                num = 0
        else:
            target = key[1:]
            key = key[0:1]
            num = 1
    if  (key[0:1] == "@") and key[1:] != "":
        if  key.find(" ") != -1:
            try:
                num = int(key[key.find(" ")+1:])
                target = key[1:key.find(" ")]
                key = key[0:1]
            except: 
                num = 0
        else:
            target = key[1:]
            key = key[0:1]
            num = 1
    if  (key[0:4] == "LOVE") and key[4:] != "":
        try:
            num = int(key[4:])
        except:
            num = -1
    if  (key[0:3] == "IUU" or key[0:3] == "UUU"):
        try:
            num = int(key[3:])
        except:
            num = -1
        if key[3:] == "":
            num = 0
    elif  (key[0:2] == "IU" or key[0:2] == "UU") and key[2:] != "":
        try:
            num = int(key[2:])
        except:
            num = -1
    if  key[0:2] == "MM" and key[2:] != "":
        try:
            num = int(key[2:])
        except:
            num = -1
    if  key[0:6] == "DELETE":
        try:
            num = int(key[6:])
        except:
            num =-1
    # Call back start
    if  key == "HELP" or key == "H" or key == "-H": # Help for IU 
        Strrr = "IU Line Bot v2.9" + "\ n" \
                "IU: สุ่ม IU" + "\ n" \
                "UU 5: IU คนที่ 5 จากด้านล่าง" + "\ n" \
                "UUU 5: IU หมายเลข 5 ที่ฉันชอบ" + "\ n" \
                "Love 2: เพิ่ม IU คนที่สองในรายการโปรด" + "\ n" \
                "ลบ 1: ลบภาพแรกจากด้านล่าง" + "\ n" \
                "OO: ยุโรปและอเมริกา" + "\ n" \
                "CC: คอสเพลย์" + "\ n" \
                "MM: สาวไต้หวัน" + "\ n" \
                "PP: 18 แบน" + "\ n" \
                "วางลิงก์ IG เพื่อวิเคราะห์รูปภาพเดียวรูปภาพวิดีโอหลายภาพและการเปลี่ยนแปลงที่ จำกัด เวลาโดยอัตโนมัติจากนั้นขยายออก" + "\ n" \
                "วางลิงก์ vibrato และขยายโดยอัตโนมัติ" + "\ n" \
                "วางลิงก์ Youtube เพื่อขยายอัตโนมัติ" + "\ n" \
                "วางลิงก์ moptt เพื่อขยายรูปภาพโดยอัตโนมัติ" + "\ n" \
                "สภาพอากาศ: สภาพอากาศปัจจุบันในไทเป" + "\ n" \
                "#iu: ค้นหา IG ล่าสุด #iu" + "\ n" \
                "#iu 10: ค้นหา #iu 10 ล่าสุด" + "\ n" \
                "@iu: ค้นหา IG ล่าสุด @iu" + "\ n" \
                "@iu 10: ค้นหา @iu 10 ล่าสุด" + "\ n" \
                "การรับประทานอาหารเป็นภาษาอังกฤษ: การแปลมื้ออาหารเป็นภาษาอังกฤษรองรับภาษาจีนอังกฤษญี่ปุ่นเกาหลีจีนตัวย่อ" + "\ n" \
                "ออกเสียงภาษาเกาหลีว่ากิน: แปลมื้ออาหารเป็นภาษาเกาหลีและออกเสียงเป็นภาษาเกาหลี"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=Strrr))
    if  key[0:28] == "https://www.instagram.com/p/": # Instagram
        shortcode = key[28:39]
        sub_page = "https://www.instagram.com/p/" + shortcode +"/"
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'cookie': 'sessionid=YOUR SISSION'
        }
        Login_test =0
        while Login_test != -1:
            try:
                r = requests.get(sub_page,headers=headers)
                Login_test = r.text.find("Login • Instagram")
                # print(Login_test)
            except:
                Login_test = -1
        url_list =[]
        start = 0
        video = 0
        video = r.text.find('video_url":')
        if video != -1:
            start = r.text.find('video_url":')+12
            end = r.text.find('"video_view_count"')-2
            url_video = r.text[start:end].replace("\\u0026","&")
            # print(url_video)
            # print(url_video)
            start = r.text.find('display_url":"') + 14
            end = r.text.find(',"display_resources"')-1
            url_display = r.text[start:end].replace("\\u0026","&")
            # print(url_display)
            # print(url_display)
            line_bot_api.reply_message(event.reply_token,VideoSendMessage(original_content_url=url_video,preview_image_url=url_display))
        else:
            for i in range(1,12):
                if start != 13:
                    start = r.text.find("display_url",start)+14
                else:
                    pass
                if start != 13:
                    end = r.text.find("display_resources",start)-3
                    # print(start)
                    # print(end)
                    # print(r.text[start:end].replace("\\u0026","&"))
                    # print(r.text[start:end].replace("\\u0026","&"))
                    url_list.append(r.text[start:end].replace("\\u0026","&"))
                else:
                    pass
            # print(url_list)
            if len(url_list)>2:
                # out_temp=[]
                bubble_container = []
                for i in range(1,len(url_list)):
                    container = BubbleContainer(size="giga",hero=ImageComponent(url=url_list[i],size='full',aspect_mode='cover',action=URIAction(uri=url_list[i])))
                    bubble_container.append(container)
                line_bot_api.reply_message(event.reply_token,
                    FlexSendMessage(alt_text="Multiple pictures",
                        contents=CarouselContainer(contents=bubble_container)
                    )
                )
            else:
                line_bot_api.reply_message(event.reply_token,
                ImageSendMessage(original_content_url= url_list[0], preview_image_url=url_list[0])
                )
    if  key[0:30] == "https://instagram.com/stories/": # IG time limit
        story_num = key[key.find("/",30)+1:key.find("?")]
        input_url = key[0:key.find("/",30)+1] + story_num
        r = requests.get(input_url).text
        reel_start = r.find(':{"id":')+8
        reel_end = r.find(',"profile_pic_url":')-1
        reel_ids = str(r[reel_start:reel_end])
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'cookie': 'sessionid=1169657472%3AnU3Lul6G0ZKmB1%3A18'
        }
        hash_IG = "YOUR HASH" #5/20
        query_url = "https://www.instagram.com/graphql/query/?query_hash="+hash_IG+"&variables=%7B%22"+"reel_ids%22%3A%5B%22"+reel_ids +"%22%5D%2C%22tag_names%22%3A%5B%5D%2C%22location_ids%22%3A%5B%5D%2C%22highlight_reel_ids%22%3A%5B%5D%2C%22precomposed_overlay%22%3Afalse%2C%22show_story_viewer_list%22%3Atrue%2C%22story_viewer_fetch_count%22%3A200%2C%22story_viewer_cursor%22%3A%22%22%2C%22stories_video_dash_manifest%22%3Afalse%7D"
        r = requests.get(query_url,headers=headers)
        IG_items = []
        stories_nums = len(r.json()['data']['reels_media'][0]['items'])
        for i in range(stories_nums):
            IG_items.append(r.json()['data']['reels_media'][0]['items'][i]['id'])
        story_num = IG_items.index(story_num)
        try:
            v_or_p = 1
            output_url = r.json()['data']['reels_media'][0]['items'][story_num]['video_resources'][1]['src']
            url_display = r.json()['data']['reels_media'][0]['items'][story_num]['display_url']
        except:
            try:
                v_or_p = 1
                output_url = r.json()['data']['reels_media'][0]['items'][story_num]['video_resources'][0]['src']
                url_display = r.json()['data']['reels_media'][0]['items'][story_num]['display_url']
            except:
                v_or_p = 2
                output_url = r.json()['data']['reels_media'][0]['items'][story_num]['display_url']
                url_display = output_url
        if v_or_p ==1:
            line_bot_api.reply_message(event.reply_token,VideoSendMessage(original_content_url=output_url,preview_image_url=url_display))
        else:
            line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=output_url,preview_image_url=url_display))
    if  key[0:21] == "https://v.douyin.com/": # DouYin video
        input_url = key
        headers = {
            'user-agent': 'PostmanRuntime/7.24.1'
        }
        redirect_url = requests.get(input_url).url
        item_ids = redirect_url[38:57]
        r = requests.get(redirect_url,headers=headers)
        dytk_start = r.text.find("dytk: ")+7
        dytk_end = r.text.find(",",r.text.find("dytk: "))-1
        dytk = r.text[dytk_start:dytk_end]
        input_url = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids="+ item_ids + "&dytk=" + dytk
        r = requests.get(input_url,headers=headers)
        output_url = r.json()['item_list'][0]['video']['play_addr']['url_list'][0]
        url_display = r.json()['item_list'][0]['video']['cover']['url_list'][0]
        url_display = url_display.replace("300x400","540x960")
        r = requests.get(url_display)
        if r.text.find("Fail to handle imagesite request")>1:
            url_display = url_display.replace("540x960","300x400")
        line_bot_api.reply_message(event.reply_token,VideoSendMessage(original_content_url=output_url,preview_image_url=url_display))
    if  key[0:25] == "https://www.facebook.com/": # FB video
        input_url = key.strip('\n')
        r = requests.get(input_url)
        if r.text.find("hd_src") != -1:
            output_url = re.search('hd_src:"(.+?)"', r.text).group(1)
            display_url = re.search('spriteIndexToURIMap:{(.+?)}', r.text)[1][5:-1]
            line_bot_api.reply_message(event.reply_token,VideoSendMessage(original_content_url=output_url,preview_image_url=display_url))
        else:
            start = r.text.find("og:image")+19
            end = r.text.find(" />",start+1)-1
            output_url =  r.text[start:end]
            output_url = output_url.replace("&amp;","&")
            display_url = output_url
            line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=output_url,preview_image_url=display_url))
    if  key.find("youtu") != -1: # Youtube video
        input_url = key
        yt = YouTube(input_url)
        output_url = yt.streams[0].url
        if input_url.find('youtube') != -1:
            start = input_url.find("v=")+2
            end =start +11
            display_url = "https://i.ytimg.com/vi/" + input_url[start:end] + "/0.jpg"
        else:
            start = input_url.find(".be/")+4
            end =start +11
            display_url = "https://i.ytimg.com/vi/" + input_url[start:end] + "/0.jpg"
        line_bot_api.reply_message(event.reply_token,VideoSendMessage(original_content_url=output_url,preview_image_url=display_url),True)
    if  key.find('moptt') != -1: # MoPtt image
        input_url = key
        input_url =input_url.replace('/p/','/ptt/')
        bubble_container =[]
        output_url = json.loads(requests.get(input_url).text)
        loop_times = output_url['content'].count('.jpg')
        if loop_times >10: 
            loop_times = 10
        start = 0
        for i in range(loop_times):
            start = output_url['content'].find('https',start+1)
            end = output_url['content'].find('.jpg',start) +4
            if output_url['content'][start:end].find('.gif') == -1:
                container = BubbleContainer(size="giga",hero=ImageComponent(url=output_url['content'][start:end],size='full',aspect_mode='cover',action=URIAction(uri=output_url['content'][start:end])))
                bubble_container.append(container)
        line_bot_api.reply_message(event.reply_token,
            FlexSendMessage(alt_text="Multiple pictures",
                contents=CarouselContainer(contents=bubble_container)
            )
        )
    if  key =="#" and target != "" and num != 0: # IG tag
        if str.upper(target) == "IU" or str.upper(target) =="UU":
            target = "dlwlrma"
        Main_page = "https://www.instagram.com/explore/tags/" + target + "/?hl=zh-tw"
        r=requests.get(Main_page)
        start = 0
        for i in range(num):
            start = r.text.find("shortcode",start)+12
        end = start +11
        shortcode = r.text[start:end]
        sub_page = "https://www.instagram.com/p/" + shortcode +"/"
        r=requests.get(sub_page)
        start = r.text.find("https://in")
        end = r.text.find('<meta property="og:description"')-9
        url_tag = r.text[start:end]
        line_bot_api.reply_message(event.reply_token,
        ImageSendMessage(original_content_url= url_tag, preview_image_url=url_tag)
        )
    if  (key[0:4] == "LOVE") and num != -1 : # add to IU love list
        if  int(num)>0: 
            # line_bot_api.reply_message(event.reply_token,TextSendMessage(text=num))
            f = open(pyPath + "/urls_last.txt","r", encoding='UTF-8') 
            readFile = f.readlines()
            f.close
            url_IU = readFile[int(num)-1].strip('\n')
            
            f = open(pyPath + "/urls_love.txt","a", encoding='UTF-8') 
            f.write(str(url_IU) + '\n')
            f.close
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="I love U"))
    if  (key[0:3] == "IUU" or key[0:3] == "UUU") and num != -1 : # call IU love list
        if  int(num)>0:  
            f = open(pyPath + "/urls_love.txt","r", encoding='UTF-8') 
            readFile = f.readlines()
            f.close
            url_IU = readFile[int(num)-1]
            line_bot_api.reply_message(event.reply_token,
            ImageSendMessage(original_content_url= url_IU, preview_image_url=url_IU)
            )
        elif int(num) == 0:
            f = open(pyPath + "/urls_love.txt","r", encoding='UTF-8') 
            readFile = f.readlines()
            f.close
            to = chat_fromID
            Loop_times = len(readFile)//10+1
            for ii in range(Loop_times):
                bubble_container = []
                loop_start = ii*10
                if ii+1 == Loop_times:
                    loop_end = len(readFile)
                else:
                    loop_end = (ii+1)*10
                for i in range(loop_start,loop_end):
                    container = BubbleContainer(size="giga",hero=ImageComponent(url=readFile[i].strip('\n'),size='full',aspect_mode='cover',action=URIAction(uri=readFile[i].strip('\n'))))
                    bubble_container.append(container)
                line_bot_api.push_message(to,
                    FlexSendMessage(alt_text="Multiple pictures",
                        contents=CarouselContainer(contents=bubble_container)
                    )
                )
    elif  (key[0:2] == "IU" or key[0:2] == "UU") and num != -1 : # call IU random list
        if  int(num)>0:  
            # print(num)
            f = open(pyPath + "/urls_last.txt","r", encoding='UTF-8') 
            readFile = f.readlines()
            f.close
            url_IU = readFile[int(num)-1]
            line_bot_api.reply_message(event.reply_token,
            ImageSendMessage(original_content_url= url_IU, preview_image_url=url_IU)
            )
        else:
            f = open(pyPath + "/urls_IU.txt","r", encoding='UTF-8')
            readFile = f.readlines()
            f.close
            url_IU = readFile[random.randint(0,len(readFile))].strip('\n')
            line_bot_api.reply_message(event.reply_token,
            ImageSendMessage(original_content_url= url_IU, preview_image_url=url_IU)
            )
            f = open(pyPath + "/urls_last.txt","r", encoding='UTF-8') 
            readFile = f.readlines()
            f.close
            f = open(pyPath + "/urls_last.txt","w", encoding='UTF-8') 
            f.write(str(url_IU) + '\n')
            for line in readFile:
                f.write(line)
        f.close
    if key[0:6] == 'DELETE' and num != -1: # delete IU from random list
        num = int(num) -1
        f = open(pyPath + "/urls_last.txt","r", encoding='UTF-8') 
        readFile = f.readlines()
        url = str(readFile[num])
        f.close
        f = open(pyPath + "/urls_IU.txt","r", encoding='UTF-8')
        readFile = f.readlines()
        f.close
        f = open(pyPath + "/urls_IU.txt","w", encoding='UTF-8')
        for line in readFile:
            if line != url:
                f.write(line)
        f.close
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="Delete! ok!"))
    if  key[0:2] == "MM" and num != -1: # call TW mm
        f = open(pyPath + "/JKF_MM_urls.txt","r", encoding='UTF-8')
        readFile = f.readlines()
        f.close
        if key == "MM":
            num = random.randint(0,len(readFile))
        main_Page = "https://www.mymypic.net/data/attachment/forum/"
        url = main_Page + readFile[num].strip('\n')
        line_bot_api.reply_message(event.reply_token,
        ImageSendMessage(original_content_url= url, preview_image_url=url)
        )
    if  key == "PP": # call PP sex
        f = open(pyPath + "/JKF_AV_urls.txt","r", encoding='UTF-8')
        readFile = f.readlines()
        f.close
        num = random.randint(0,len(readFile))
        main_Page = "https://www.mymypic.net/data/attachment/forum/"
        url = main_Page + readFile[num].strip('\n')
        line_bot_api.reply_message(event.reply_token,
        ImageSendMessage(original_content_url= url, preview_image_url=url)
        )
    if  key == "OO": # call OO foreigner
        f = open(pyPath + "/JKF_OO_urls.txt","r", encoding='UTF-8')
        readFile = f.readlines()
        f.close
        num = random.randint(0,len(readFile))
        main_Page = "https://www.mymypic.net/data/attachment/forum/"
        url = main_Page + readFile[num].strip('\n')
        line_bot_api.reply_message(event.reply_token,
        ImageSendMessage(original_content_url= url, preview_image_url=url)
        )
    if  key == "CC": # call cosplay 
        f = open(pyPath + "/JKF_CC_urls.txt","r", encoding='UTF-8')
        readFile = f.readlines()
        f.close
        num = random.randint(0,len(readFile))
        main_Page = "https://www.mymypic.net/data/attachment/forum/"
        url = main_Page + readFile[num].strip('\n')
        line_bot_api.reply_message(event.reply_token,
        ImageSendMessage(original_content_url= url, preview_image_url=url)
        )
    if  key == "CCC": # call team for Luna
        f = open(pyPath + "/urls_CCC.txt","r", encoding='UTF-8')
        readFile = f.readlines()
        f.close
        num = random.randint(0,len(readFile))
        url = readFile[num].strip('\n')
        line_bot_api.reply_message(event.reply_token,
        ImageSendMessage(original_content_url= url, preview_image_url=url)
        )
    if  key == "CCCC": # call team for high
        f = open(pyPath + "/urls_CCCC.txt","r", encoding='UTF-8')
        readFile = f.readlines()
        f.close
        num = random.randint(0,len(readFile))
        url = readFile[num].strip('\n')
        line_bot_api.reply_message(event.reply_token,
        ImageSendMessage(original_content_url= url, preview_image_url=url)
        )
    if  key == "CUTE": # call cute sticker 
        line_bot_api.reply_message(event.reply_token, StickerSendMessage(package_id=11537, sticker_id=52002747))
    if  key == "DEAD": # call dead sticker
        line_bot_api.reply_message(event.reply_token, StickerSendMessage(package_id=11537, sticker_id=52002757))
    if  key[0:2] =="發音": # call translater and spaker
        translator = Translator()
        text_out = str(translator.translate(key[6:],dest=LanguageList[LanguageList.index(key[3:5])+1]))
        start = text_out.find("text=")+5
        end = text_out.find("pronunciation=")-2
        if key[3:5] in LanguageList:
            tts = gTTS(text_out[start:end],lang=LanguageList[LanguageList.index(key[3:5])+1])
            url_audio = str(tts.get_urls()[0]) + ".mp3"
            line_bot_api.reply_message(event.reply_token,AudioSendMessage(original_content_url=url_audio, duration=100000))
        else:
            tts = gTTS(key[2:])
            url_audio = str(tts.get_urls()[0]) + ".mp3"
            line_bot_api.reply_message(event.reply_token,AudioSendMessage(original_content_url=url_audio, duration=100000))
    if  key[0:2] in LanguageList and key[2] == " ": # call google translater
        translator = Translator()
        text_out = str(translator.translate(key[3:],dest=LanguageList[LanguageList.index(key[0:2])+1]))
        start = text_out.find("text=")+5
        end = text_out.find("pronunciation=")-2
        # print(text_out)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out[start:end]))
        # line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=2))
    if  key == "天氣" or key == "WEATHER": # IU Weather
        f = open(pyPath + "/urls_IU.txt","r", encoding='UTF-8')
        readFile = f.readlines()
        f.close
        url_IU = readFile[random.randint(0,len(readFile))].strip('\n')
        w_page = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-061?Authorization=YOURAUTHORIZATION&locationName=%E5%A3%AB%E6%9E%97%E5%8D%80"
        r = json.loads(requests.get(w_page).text)
        _0_time_s = str(r['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][0]['startTime'][11:13])
        _0_time_e = str(r['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][0]['endTime'][11:13])
        _1_time_s = str(r['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][1]['startTime'][11:13])
        _1_time_e = str(r['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][1]['endTime'][11:13])
        _2_time_s = str(r['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][2]['startTime'][11:13])
        _2_time_e = str(r['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][2]['endTime'][11:13])
        _3_time_s = str(r['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][3]['startTime'][11:13])
        _3_time_e = str(r['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][3]['endTime'][11:13])
        _4_time_s = str(r['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][4]['startTime'][11:13])
        _4_time_e = str(r['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][4]['endTime'][11:13])
        _5_time_s = str(r['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][5]['startTime'][11:13])
        _5_time_e = str(r['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][5]['endTime'][11:13])
        _0_decrip = str(r['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][0]['elementValue'][0]['value'])
        _1_decrip = str(r['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][1]['elementValue'][0]['value'])
        _2_decrip = str(r['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][2]['elementValue'][0]['value'])
        _3_decrip = str(r['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][3]['elementValue'][0]['value'])
        _4_decrip = str(r['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][4]['elementValue'][0]['value'])
        _5_decrip = str(r['records']['locations'][0]['location'][0]['weatherElement'][1]['time'][5]['elementValue'][0]['value'])
        _0_temp = str(r['records']['locations'][0]['location'][0]['weatherElement'][3]['time'][0]['elementValue'][0]['value'])
        _1_temp = str(r['records']['locations'][0]['location'][0]['weatherElement'][3]['time'][1]['elementValue'][0]['value'])
        _2_temp = str(r['records']['locations'][0]['location'][0]['weatherElement'][3]['time'][2]['elementValue'][0]['value'])
        _3_temp = str(r['records']['locations'][0]['location'][0]['weatherElement'][3]['time'][3]['elementValue'][0]['value'])
        _4_temp = str(r['records']['locations'][0]['location'][0]['weatherElement'][3]['time'][4]['elementValue'][0]['value'])
        _5_temp = str(r['records']['locations'][0]['location'][0]['weatherElement'][3]['time'][5]['elementValue'][0]['value'])
        _0_humidity = str(r['records']['locations'][0]['location'][0]['weatherElement'][4]['time'][0]['elementValue'][0]['value'])
        _1_humidity = str(r['records']['locations'][0]['location'][0]['weatherElement'][4]['time'][1]['elementValue'][0]['value'])
        _2_humidity = str(r['records']['locations'][0]['location'][0]['weatherElement'][4]['time'][2]['elementValue'][0]['value'])
        _3_humidity = str(r['records']['locations'][0]['location'][0]['weatherElement'][4]['time'][3]['elementValue'][0]['value'])
        _4_humidity = str(r['records']['locations'][0]['location'][0]['weatherElement'][4]['time'][4]['elementValue'][0]['value'])
        _5_humidity = str(r['records']['locations'][0]['location'][0]['weatherElement'][4]['time'][5]['elementValue'][0]['value'])
        _0_feel = str(r['records']['locations'][0]['location'][0]['weatherElement'][5]['time'][0]['elementValue'][1]['value'])
        _1_feel = str(r['records']['locations'][0]['location'][0]['weatherElement'][5]['time'][1]['elementValue'][1]['value'])
        _2_feel = str(r['records']['locations'][0]['location'][0]['weatherElement'][5]['time'][2]['elementValue'][1]['value'])
        _3_feel = str(r['records']['locations'][0]['location'][0]['weatherElement'][5]['time'][3]['elementValue'][1]['value'])
        _4_feel = str(r['records']['locations'][0]['location'][0]['weatherElement'][5]['time'][4]['elementValue'][1]['value'])
        _5_feel = str(r['records']['locations'][0]['location'][0]['weatherElement'][5]['time'][5]['elementValue'][1]['value'])
        _0_rain = str(r['records']['locations'][0]['location'][0]['weatherElement'][7]['time'][0]['elementValue'][0]['value'])
        _1_rain = str(r['records']['locations'][0]['location'][0]['weatherElement'][7]['time'][0]['elementValue'][0]['value'])
        _2_rain = str(r['records']['locations'][0]['location'][0]['weatherElement'][7]['time'][1]['elementValue'][0]['value'])
        _3_rain = str(r['records']['locations'][0]['location'][0]['weatherElement'][7]['time'][1]['elementValue'][0]['value'])
        _4_rain = str(r['records']['locations'][0]['location'][0]['weatherElement'][7]['time'][2]['elementValue'][0]['value'])
        _5_rain = str(r['records']['locations'][0]['location'][0]['weatherElement'][7]['time'][2]['elementValue'][0]['value'])
        _0_wind = str(r['records']['locations'][0]['location'][0]['weatherElement'][8]['time'][0]['elementValue'][0]['value'])
        _1_wind = str(r['records']['locations'][0]['location'][0]['weatherElement'][8]['time'][1]['elementValue'][0]['value'])
        _2_wind = str(r['records']['locations'][0]['location'][0]['weatherElement'][8]['time'][2]['elementValue'][0]['value'])
        _3_wind = str(r['records']['locations'][0]['location'][0]['weatherElement'][8]['time'][3]['elementValue'][0]['value'])
        _4_wind = str(r['records']['locations'][0]['location'][0]['weatherElement'][8]['time'][4]['elementValue'][0]['value'])
        _5_wind = str(r['records']['locations'][0]['location'][0]['weatherElement'][8]['time'][5]['elementValue'][0]['value'])
        _0_wind_d = str(r['records']['locations'][0]['location'][0]['weatherElement'][9]['time'][0]['elementValue'][0]['value'])
        _1_wind_d = str(r['records']['locations'][0]['location'][0]['weatherElement'][9]['time'][1]['elementValue'][0]['value'])
        _2_wind_d = str(r['records']['locations'][0]['location'][0]['weatherElement'][9]['time'][2]['elementValue'][0]['value'])
        _3_wind_d = str(r['records']['locations'][0]['location'][0]['weatherElement'][9]['time'][3]['elementValue'][0]['value'])
        _4_wind_d = str(r['records']['locations'][0]['location'][0]['weatherElement'][9]['time'][4]['elementValue'][0]['value'])
        _5_wind_d = str(r['records']['locations'][0]['location'][0]['weatherElement'][9]['time'][5]['elementValue'][0]['value'])
        bubble_container=[]
        container = BubbleContainer(
            size="giga",
            hero=ImageComponent(
                url=url_IU,
                size='full',
                aspect_mode='cover',
                action=URIAction(
                    uri=url_IU
                )
            ),
            body=BoxComponent(
                layout='vertical',
                margin="none",
                contents=[
                    BoxComponent(
                        layout='baseline',
                        margin="md",
                        contents=[
                            TextComponent(text="時間", size='sm'),
                            TextComponent(text="溫度", size='sm'),
                            TextComponent(text="降雨", size='sm'),
                            # TextComponent(text="溼度", size='sm'),
                            TextComponent(text="風力", size='sm'),
                            TextComponent(text="風向", size='sm'),
                            # TextComponent(text="舒適", size='sm'),
                            TextComponent(text="型態", size='sm')
                        ]
                    ),
                    SeparatorComponent(margin="md"),
                    BoxComponent(
                        layout='baseline',
                        margin="md",
                        contents=[
                            TextComponent(text=_0_time_s + "-" + _0_time_e, size='sm'),
                            TextComponent(text=_0_temp +" ℃", size='sm'),
                            TextComponent(text=_0_rain + " %", size='sm'),
                            # TextComponent(text=_0_humidity+ " %", size='sm'),
                            TextComponent(text=_0_wind + " m/s", size='sm'),
                            TextComponent(text=_0_wind_d.replace('風',''), size='sm'),
                            # TextComponent(text=_0_feel, size='sm'),
                            TextComponent(text=_0_decrip.replace('午後短暫',''), size='sm')
                        ]
                    ),
                    SeparatorComponent(margin="md"),
                    BoxComponent(
                        layout='baseline',
                        margin="md",
                        contents=[
                            TextComponent(text=_1_time_s + "-" + _1_time_e, size='sm'),
                            TextComponent(text=_1_temp +" ℃", size='sm'),
                            TextComponent(text=_1_rain + " %", size='sm'),
                            # TextComponent(text=_1_humidity+ " %", size='sm'),
                            TextComponent(text=_1_wind + " m/s", size='sm'),
                            TextComponent(text=_1_wind_d.replace('風',''), size='sm'),
                            # TextComponent(text=_1_feel, size='sm'),
                            TextComponent(text=_1_decrip.replace('午後短暫',''), size='sm',align='start')
                        ]
                    ),
                    SeparatorComponent(margin="md"),
                    BoxComponent(
                        layout='baseline',
                        margin="md",
                        contents=[
                            TextComponent(text=_2_time_s + "-" + _2_time_e, size='sm'),
                            TextComponent(text=_2_temp +" ℃", size='sm'),
                            TextComponent(text=_2_rain + " %", size='sm'),
                            # TextComponent(text=_2_humidity+ " %", size='sm'),
                            TextComponent(text=_2_wind + " m/s", size='sm'),
                            TextComponent(text=_2_wind_d.replace('風',''), size='sm'),
                            # TextComponent(text=_2_feel, size='sm'),
                            TextComponent(text=_2_decrip.replace('午後短暫',''), size='sm',align='start')
                        ]
                    ),
                    SeparatorComponent(margin="md"),
                    BoxComponent(
                        layout='baseline',
                        margin="md",
                        contents=[
                            TextComponent(text=_3_time_s + "-" + _3_time_e, size='sm'),
                            TextComponent(text=_3_temp +" ℃", size='sm'),
                            TextComponent(text=_3_rain + " %", size='sm'),
                            # TextComponent(text=_3_humidity+ " %", size='sm'),
                            TextComponent(text=_3_wind + " m/s", size='sm'),
                            TextComponent(text=_3_wind_d.replace('風',''), size='sm'),
                            # TextComponent(text=_3_feel, size='sm'),
                            TextComponent(text=_3_decrip.replace('午後短暫',''), size='sm',align='start')
                        ]
                    ),
                ],
            )
        )
        bubble_container.append(container)
        # to = "C751440a6c38ad6d7e4ac80743e0e50ea"
        to = chat_fromID
        line_bot_api.push_message(to,FlexSendMessage(alt_text="Weather",
                contents=CarouselContainer(contents=bubble_container)
        )
        )
    if  key == "TEST": #test
        key_Push = "Push : " + str(chat_fromID)
        key_Reply = "Reply : " + str(chat_userID)
        to = chat_fromID
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=to))
    ### chat log
    if chat_fromID != "":
        chat_time = str(chat_time)
        chat_time = int(chat_time[0:10])
        chat_time = str(datetime.datetime.fromtimestamp(chat_time))
        f = open(pyPath + "/chat_log.txt","r", encoding='UTF-8')
        readFile = f.readlines()
        f.close
        chat_fromID_line = 0
        for i in range(len(readFile)):
            if chat_fromID_line == 0:
                if readFile[i][0:33] == chat_fromID:
                    chat_fromID_line = 1
                    chat_lines = int(readFile[i][36:].strip('\n'))
                    readFile.remove(chat_fromID + " : " + str(chat_lines) +'\n')
                    readFile.insert(i,chat_fromID  + " : " + str(chat_lines+1) +'\n')
                    readFile.insert(i+chat_lines+1,'\t' + chat_time + " : " + chat_userID + " : " + chat_text.replace('\n',' ') + "\n")
                    f = open(pyPath + "/chat_log.txt","w", encoding='UTF-8')
                    readFile ="".join(readFile)
                    f.write(readFile)
                    f.close
                elif i == len(readFile)-1:
                    chat_lines = 1
                    f = open(pyPath + "/chat_log.txt","a", encoding='UTF-8')
                    f.write(chat_fromID + " : " + str(chat_lines) + "\n")
                    f.write('\t' + chat_time + " : " + chat_userID + " : " + chat_text.replace('\n',' ') + "\n")
                    f.close

if  __name__ == "__main__":
    # app.debug = True
    app.run()
