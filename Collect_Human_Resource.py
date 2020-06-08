import requests
import json
import datetime
from time import sleep
import re
from fontTools.ttLib import TTFont
from bs4 import BeautifulSoup
import wget
import pytesseract
from PIL import Image
import os
pyPath = os.path.dirname(os.path.abspath(__file__))
print(pyPath)
for xxXxx in range(0,150):
    print("Now is Page: " + str(xxXxx))
    url_now = "https://www.1111.com.tw/search/job?ks=%E9%9B%BB%E8%A9%B1%E8%A1%8C%E9%8A%B7%E4%BA%BA%E5%93%A1&fs=1&page=" + str(xxXxx)
    r = requests.get(url_now)
    soup = BeautifulSoup(r.text, 'html.parser')
    text_list = soup.find_all('div',class_="position0")
    corp_list = soup.find_all('a',class_="fanshome")
    for iii in range(len(text_list)):  ###len(text_list)
        print("Now is Page "+ str(xxXxx) + " and Job: " + str(iii))
        job_title = str(text_list[iii])[str(text_list[iii]).find('title=')+7:str(text_list[iii]).find('"',str(text_list[iii]).find('title=')+7)]
        job_url = "https://www.1111.com.tw/job/" + str(text_list[iii])[str(text_list[iii]).find('href=')+11:str(text_list[iii]).find('"',str(text_list[iii]).find('href=')+11)]
        corp_url = "https://www.1111.com.tw/corp/" + str(corp_list[iii])[str(corp_list[iii]).find('data-fanshome=')+15:str(corp_list[iii]).find('"',str(corp_list[iii]).find('data-fanshome=')+15)] + "/"
        print(job_url)
        # print(corp_url)
        r = requests.get(job_url)
        woff_url = r.text[r.text.find("<link href=")+12:r.text.find(".css",r.text.find("<link href=")+12)] + ".woff?v0001"
        if r.text.find('<li class="paddingLB">') != -1:
            job_desciption = r.text[r.text.find('<li class="paddingLB">')+22:r.text.find('</li>',r.text.find('<li class="paddingLB">')+22)].replace('\n',"")
        else:
            job_desciption = "No Job desciption"
        if r.text.find('ftbrown listContent') != -1:
            job_contact = r.text[r.text.find('ftbrown listContent')+21:r.text.find('<',r.text.find('ftbrown listContent')+21)].replace("0","").replace("1","").replace("2","").replace("3","").replace("4","").replace("5","").replace("6","").replace("7","").replace("8","").replace("9","").replace(":","")
        else:
            job_contact = "No Job contacr"
        if r.text.find('更新日期'):
            job_update = r.text[r.text.find('更新日期')+5:r.text.find('【',r.text.find('更新日期')+5)]
        else:
            job_update = "No Job update"
        job_mail = r.text.find('電子郵件：')
        job_phone = r.text.find('市話聯絡：')
        job_cellphone = r.text.find('手機聯絡：')
        if job_mail == -1 and job_phone ==-1 and job_cellphone == -1:
            pass
        else:
            wget.download(woff_url, pyPath + '/temp.woff')
            font = TTFont(pyPath + '/temp (1).woff')
            font.saveXML(pyPath + '/temp.xml')
            print("")
        if job_mail !=-1:
            job_mail = r.text[r.text.find('電子郵件：')+44:r.text.find('<',r.text.find('電子郵件：')+44)]
            job_mail = job_mail[::2]
            f = open(pyPath + "/unicode_PUA.txt","r", encoding='UTF-8')
            unicode_table = f.readlines()
            f.close
            job_mail_out = ""
            for ii_mail in range(len(job_mail)):
                Aaa = job_mail[ii_mail]+'\n'
                findit = unicode_table.index(Aaa)+1
                unicode_out = "0x" + unicode_table[findit].strip('\n')
                unicode_out = unicode_out.lower()
                # print(unicode_out)
                f = open(pyPath +  '/temp.xml',"r", encoding='UTF-8')
                readFile = f.read()
                f.close
                soup = BeautifulSoup(readFile, 'xml')
                list_uniMap = soup.find_all('map')
                list_uniMap_code = []
                list_uniMap_name = []
                for i in range(len(list_uniMap)):
                    list_uniMap_code.append(list_uniMap[i].get('code'))
                for i in range(len(list_uniMap)):
                    list_uniMap_name.append(list_uniMap[i].get('name'))
                map_out = list_uniMap_name[list_uniMap_code.index(unicode_out)]
                # print(map_out)
                list_all = soup.find_all('TTGlyph')
                list_name =[]
                for i in range(len(list_all)):
                    list_name.append(list_all[i].get('name'))
                xMin = str(list_all[list_name.index(map_out)].get('xMin'))
                xMax = str(list_all[list_name.index(map_out)].get('xMax'))
                yMin = str(list_all[list_name.index(map_out)].get('yMin'))
                yMax = str(list_all[list_name.index(map_out)].get('yMax'))
                id_para = xMin + xMax + yMin + yMax + '\n'
                # print(id_para.strip('\n'))
                f = open(pyPath +  '/id_para.txt',"r", encoding='UTF-8')
                id_para_table = f.readlines()
                f.close
                str_out = id_para_table[id_para_table.index(id_para)-1].strip('\n')
                # print(str_out)
                job_mail_out = job_mail_out +str_out
                job_mail_output = job_mail_out
        else:
            job_mail_output = "No Job mail"
        # print(job_mail_output)
        if job_phone !=-1:
            job_phone = r.text[r.text.find('市話聯絡：')+44:r.text.find('<',r.text.find('市話聯絡：')+44)]
            job_phone = job_phone[::2]
            f = open(pyPath +  '/unicode_PUA.txt',"r", encoding='UTF-8')
            unicode_table = f.readlines()
            f.close
            job_phone_out = ""
            for ii_phone in range(len(job_phone)):
                Aaa = job_phone[ii_phone]+'\n'
                findit = unicode_table.index(Aaa)+1
                unicode_out = "0x" + unicode_table[findit].strip('\n')
                unicode_out = unicode_out.lower()
                # print(unicode_out)
                f = open(pyPath +  '/temp.xml',"r", encoding='UTF-8')
                readFile = f.read()
                f.close
                soup = BeautifulSoup(readFile, 'xml')
                list_uniMap = soup.find_all('map')
                list_uniMap_code = []
                list_uniMap_name = []
                for i in range(len(list_uniMap)):
                    list_uniMap_code.append(list_uniMap[i].get('code'))
                for i in range(len(list_uniMap)):
                    list_uniMap_name.append(list_uniMap[i].get('name'))
                map_out = list_uniMap_name[list_uniMap_code.index(unicode_out)]
                # print(map_out)
                list_all = soup.find_all('TTGlyph')
                list_name =[]
                for i in range(len(list_all)):
                    list_name.append(list_all[i].get('name'))
                xMin = str(list_all[list_name.index(map_out)].get('xMin'))
                xMax = str(list_all[list_name.index(map_out)].get('xMax'))
                yMin = str(list_all[list_name.index(map_out)].get('yMin'))
                yMax = str(list_all[list_name.index(map_out)].get('yMax'))
                id_para = xMin + xMax + yMin + yMax + '\n'
                # print(id_para.strip('\n'))
                f = open(pyPath +  '/id_para.txt',"r", encoding='UTF-8')
                id_para_table = f.readlines()
                f.close
                str_out = id_para_table[id_para_table.index(id_para)-1].strip('\n')
                # print(str_out)
                job_phone_out = job_phone_out + str_out
                job_phone_output = job_phone_out
        else:
            job_phone_output = "No Job Phone"
        # print(job_phone_output)

        if job_cellphone !=-1:
            job_cellphone = r.text[r.text.find('手機聯絡：')+44:r.text.find('<',r.text.find('手機聯絡：')+44)]
            job_cellphone = job_cellphone[::2]
            f = open(pyPath +  '/unicode_PUA.txt',"r", encoding='UTF-8')
            unicode_table = f.readlines()
            f.close
            job_cellphone_out =""
            for ii_cellphone in range(len(job_cellphone)):
                Aaa = job_cellphone[ii_cellphone]+'\n'
                findit = unicode_table.index(Aaa)+1
                unicode_out = "0x" + unicode_table[findit].strip('\n')
                unicode_out = unicode_out.lower()
                # print(unicode_out)
                f = open(pyPath +  '/temp.xml',"r", encoding='UTF-8')
                readFile = f.read()
                f.close
                soup = BeautifulSoup(readFile, 'xml')
                list_uniMap = soup.find_all('map')
                list_uniMap_code = []
                list_uniMap_name = []
                for i in range(len(list_uniMap)):
                    list_uniMap_code.append(list_uniMap[i].get('code'))
                for i in range(len(list_uniMap)):
                    list_uniMap_name.append(list_uniMap[i].get('name'))
                map_out = list_uniMap_name[list_uniMap_code.index(unicode_out)]
                # print(map_out)
                list_all = soup.find_all('TTGlyph')
                list_name =[]
                for i in range(len(list_all)):
                    list_name.append(list_all[i].get('name'))
                xMin = str(list_all[list_name.index(map_out)].get('xMin'))
                xMax = str(list_all[list_name.index(map_out)].get('xMax'))
                yMin = str(list_all[list_name.index(map_out)].get('yMin'))
                yMax = str(list_all[list_name.index(map_out)].get('yMax'))
                id_para = xMin + xMax + yMin + yMax + '\n'
                # print(id_para.strip('\n'))
                f = open(pyPath +  '/id_para.txt',"r", encoding='UTF-8')
                id_para_table = f.readlines()
                f.close
                str_out = id_para_table[id_para_table.index(id_para)-1].strip('\n')
                # print(str_out)
                job_cellphone_out =job_cellphone_out + str_out
                job_cellphone_output = job_cellphone_out
        else:
            job_cellphone_output = "No Job CellPhone"
        # print(job_cellphone_output)
            
        r = requests.get(corp_url)
        corp_title = r.text[r.text.find('title')+6:r.text.find('</title>',r.text.find('title')+6)].replace('－1111人力銀行',"").replace("【工作職缺及徵才簡介】1111人力銀行","")
        start = r.text.find('<div class="listTitle">聯絡地址：</div><div class="listContent">')
        if start != -1:
            corp_location = r.text[r.text.find('<div class="listTitle">聯絡地址：</div><div class="listContent">')+59:r.text.find('<',r.text.find('<div class="listTitle">聯絡地址：</div><div class="listContent">')+59)]
        else:
            corp_location = "No Corp Location"
        start = r.text.find('行業別：</span></div><div class="listContent">')
        if start != -1:
            corp_category = r.text[r.text.find('target="_blank">',start)+16:r.text.find('<',r.text.find('target="_blank">',start)+16)]
        else:
            corp_category = "No Corp Category"
        start = r.text.find('行業說明：</div><div class="listContent">')
        if start != -1:
            corp_info = r.text[r.text.find('行業說明：</div><div class="listContent">')+36:r.text.find('<',r.text.find('行業說明：</div><div class="listContent">')+36)]
        else:
            corp_info = corp_category
        start = r.text.find('公司電話：</div><div class="listContent">')
        corp_phone = r.text[r.text.find('公司電話：</div><div class="listContent">')+46:r.text.find('"',r.text.find('公司電話：</div><div class="listContent">')+46)]
        if r.text.find('暫不提供電話') != -1:
            corp_phone = "暫不提供電話"
        elif start != -1 :
            corp_phone = "https://www.1111.com.tw" + corp_phone
            wget.download(corp_phone, pyPath +  '/temp_phone.png')
            print()
            img = Image.open(pyPath +  '/temp_phone (1).png')
            pix = img.load()
            # print(img.mode)
            for y in range(img.size[1]):  
                for x in range(img.size[0]):
                    if pix[x, y][3] < 255:
                        pix[x, y] = (0, 0, 0, 255)
                    else:
                        pix[x, y] = (255, 255, 255, 255)
            img = img.convert('L')
            pix = img.load()
            # img.show()
            w = img.width
            h = img.height
            # print(w)
            # print(h)
            # sto_pixel =img.getpixel((0,0))
            # print(sto_pixel)
            # f = open("C:\\Users\\Mark\\Documents\\Py_all\\test\\img.txt","w", encoding='UTF-8')
            # for i in range(h):
            #     for iiii in range(w):
            #         cur_pixel = img.getpixel((iiii,i))
            #         # print(cur_pixel)
            #         f.write(str(cur_pixel) + "\t")
            #     f.write("\n")
            # f.close
            str_edge_list =[]
            x_pre = 0
            x_now = 0
            for xx in range(w):
                y_temp = 0
                for yy in range(h):
                    y_temp = y_temp + pix[xx,yy]
                if y_temp == 0:
                    x_now = 0
                else:
                    x_now = 1
                if (x_now - x_pre) == 1:
                    x_pre = x_now
                    str_edge_list.append(xx)
                elif (x_now - x_pre) == -1:
                    x_pre = x_now
                    str_edge_list.append(xx-1)
                else:
                    x_pre = x_now
            # print(str_edge_list)
            # print(len(str_edge_list))
            f = open(pyPath +  '/phone_num.txt',"r", encoding='UTF-8')
            phone_num = f.readlines()
            f.close
            corp_phone = ""
            for edges in range(int(len(str_edge_list)/2)): #len(str_edge_list)/2
                y_temp = 0
                for xxx in range(str_edge_list[edges*2],str_edge_list[edges*2+1]+1):
                    for yyy in range(h):
                        y_temp = y_temp + pix[xxx,yyy]
                # print(y_temp)
                if y_temp == 3315:
                    y_temp2 = 0
                    for xxxx in range(str_edge_list[edges*2],str_edge_list[edges*2]+2):
                        for yyyy in range(h):
                            y_temp2 = y_temp2 + pix[xxxx,yyyy]
                    if y_temp2 == 2295:
                        digit_str = "("
                    elif y_temp2 == 1020:
                        digit_str = ")"
                    else:
                        digit_str = "1"
                elif y_temp == 6630:
                    y_temp2 = 0
                    for xxxx in range(str_edge_list[edges*2],str_edge_list[edges*2]+2):
                        for yyyy in range(h):
                            y_temp2 = y_temp2 + pix[xxxx,yyyy]
                    if y_temp2 == 1275:
                        digit_str = "4"
                    elif y_temp2 == 1785:
                        digit_str = "9"
                    else:
                        digit_str = "6"
                else:
                    Aaa = str(y_temp) + '\n'
                    findit = phone_num.index(Aaa)-1
                    digit_str = phone_num[findit].strip('\n')
                corp_phone = corp_phone + digit_str
        else:
            corp_phone = "暫不提供電話"
        # print("Phone : " + str(corp_phone))
        start = r.text.find('公司傳真：</div><div class="listContent">')
        corp_fax = r.text[r.text.find('公司傳真：</div><div class="listContent">')+46:r.text.find('"',r.text.find('公司傳真：</div><div class="listContent">')+46)]
        if r.text.find('暫不提供傳真') != -1:
            corp_fax = "暫不提供傳真"
        elif start != -1 :
            corp_fax = "https://www.1111.com.tw" + corp_fax
            wget.download(corp_fax, pyPath +  '/temp_fax.png')
            print()
            img = Image.open(pyPath +  '/temp_fax (1).png')
            pix = img.load()
            for y in range(img.size[1]):  
                for x in range(img.size[0]):
                    if pix[x, y][3] < 255:
                        pix[x, y] = (0, 0, 0, 255)
                    else:
                        pix[x, y] = (255, 255, 255, 255)
            img = img.convert('L')
            pix = img.load()
            # img.show()
            w = img.width
            h = img.height
            # print(w)
            # print(h)
            # sto_pixel =img.getpixel((0,0))
            # print(sto_pixel)
            # f = open("C:\\Users\\Mark\\Documents\\Py_all\\test\\img.txt","w", encoding='UTF-8')
            # for i in range(h):
            #     for ii in range(w):
            #         cur_pixel = img.getpixel((ii,i))
            #         # print(cur_pixel)
            #         f.write(str(cur_pixel) + "\t")
            #     f.write("\n")
            # f.close
            str_edge_list =[]
            x_pre = 0
            x_now = 0
            for xx in range(w):
                y_temp = 0
                for yy in range(h):
                    y_temp = y_temp + pix[xx,yy]
                if y_temp == 0:
                    x_now = 0
                else:
                    x_now = 1
                if (x_now - x_pre) == 1:
                    x_pre = x_now
                    str_edge_list.append(xx)
                elif (x_now - x_pre) == -1:
                    x_pre = x_now
                    str_edge_list.append(xx-1)
                else:
                    x_pre = x_now
            # print(str_edge_list)
            # print(len(str_edge_list))
            f = open(pyPath + '/phone_num.txt',"r", encoding='UTF-8')
            phone_num = f.readlines()
            f.close
            corp_fax = ""
            for edges in range(int(len(str_edge_list)/2)): #len(str_edge_list)/2
                y_temp = 0
                for xxx in range(str_edge_list[edges*2],str_edge_list[edges*2+1]+1):
                    for yyy in range(h):
                        y_temp = y_temp + pix[xxx,yyy]
                # print(y_temp)
                if y_temp == 3315:
                    y_temp2 = 0
                    for xxxx in range(str_edge_list[edges*2],str_edge_list[edges*2]+2):
                        for yyyy in range(h):
                            y_temp2 = y_temp2 + pix[xxxx,yyyy]
                    if y_temp2 == 2295:
                        digit_str = "("
                    elif y_temp2 == 1020:
                        digit_str = ")"
                    else:
                        digit_str = "1"
                elif y_temp == 6630:
                    y_temp2 = 0
                    for xxxx in range(str_edge_list[edges*2],str_edge_list[edges*2]+2):
                        for yyyy in range(h):
                            y_temp2 = y_temp2 + pix[xxxx,yyyy]
                    if y_temp2 == 1275:
                        digit_str = "4"
                    elif y_temp2 == 1785:
                        digit_str = "9"
                    else:
                        digit_str = "6"
                else:
                    Aaa = str(y_temp) + '\n'
                    findit = phone_num.index(Aaa)-1
                    digit_str = phone_num[findit].strip('\n')
                corp_fax = corp_fax + digit_str
        else:
            corp_fax = "暫不提供傳真"
        # print("Fax : " + str(corp_fax))
        f = open(pyPath + '/output.txt',"a", encoding='UTF-8')
        f.write(job_update + "\t" + corp_title + "\t" + corp_category + "\t" + corp_info + "\t" + job_mail_output + "\t" + job_title + "\t" + job_desciption+ "\t" + job_phone_output + "\t" + job_contact + "\t" + job_cellphone_output + "\t" + corp_phone + "\t" + corp_fax + "\t" + corp_location + "\t" + job_url + "\t" + corp_url + "\n")
        f.close