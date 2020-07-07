# Line_Bot_IU
Line_Bot_IU, an auto-reply bot in Line app, include functions as below:
1. Reply randomly picture with key word capturing.
2. Crawing and displaying IG, FB, Ptt, Youtube and DouYin(Tik tok).
3. Weather forecast with loctation.
4. Multiple language translator with pronunciation or spelling.

## Python + Flask + Serveo(or Ngrok)
With: line-bot-sdk-python, flask, googletrans, gtts, https://opendata.cwb.gov.tw/api

#### Text reply, Image reply, Flex reply
<img src="https://i.imgur.com/oSIJcfP.gif" width="270" height="321"><img src="https://i.imgur.com/7oFoO6s.gif" width="270" height="321"><img src="https://i.imgur.com/O5WhPqm.gif" width="270" height="321">

#### Capture IG picture, multiplo-pics, video
<img src="https://i.imgur.com/Z9TcdBA.gif" width="270" height="470"><img src="https://i.imgur.com/lC1BTDR.gif" width="270" height="470"><img src="https://i.imgur.com/WQQu8qf.gif" width="270" height="470">

#### Capture Facebook, DouYin(Tik tok), Youtube
<img src="https://i.imgur.com/BLSu29u.gif" width="270" height="470"><img src="https://i.imgur.com/vSVHlFH.gif" width="270" height="470"><img src="https://i.imgur.com/PLFW8as.gif" width="270" height="470">

#### Google translator : text to text, text to voice
<img src="https://i.imgur.com/aEiRjRr.gif" width="270" height="321"><img src="https://i.imgur.com/Ez7icPW.gif" width="270" height="321">

#### to use [Serveo](http://serveo.net/):
No installation or application just key in cmd "ssh -o ServerAliveInterval=60 -R YourDomain:80:127.0.0.1:5000 serveo.net"  
It will connect your port 5000 to the world with a specific https url(depend on your domain, and maybe your domain alreay be occupied)  
Upside: A static https url.  
Downside: ssh will automatically disconnect due to safety issue.  
to slove this problem, you can use "Autossh" but somehow it is friendly to Linux not Windows, so I make a ssh checker with python to frequently check connection.  




