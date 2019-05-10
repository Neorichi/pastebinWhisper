# -*- coding: utf-8 -*-
import bs4, requests,re, sys
import pymysql
import datetime
import time
import json
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup
import urllib.parse
import pyfiglet


_headers_get = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}

#Time API restrictions, 60 sec recommended - No more than 1000 requests per 10 minutes.
#https://pastebin.com/doc_scraping_api
time_tag = 60

#### DB Config ####
host="xxxx.xxxx.us-east-1.rds.amazonaws.com"
port=3306
dbname="xxxxx"
user="xxxxx"
password="xxxxxx"

#Example schema table
'''
CREATE TABLE `pastebin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(250),
  `line` varchar(250),
  `url` varchar(250),
  `ref` varchar(45),
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
'''

#### Telegram Config #### [Optional]
telegram_on = False
TOKEN = 'xxxxx:xxxx-xxx'
mi_canal = 11111


def searchEmail(content):
    regex = r"[\w.%+-]+@(?:[a-z\d-]+\.)+[a-z]{2,4}"
    email = re.findall(regex, str(content))
    return email

def searchEmailALine(content):
    lines = re.sub("<.*?>", " ", content)
    regex = r"[\w.%+-]+@(?:[a-z\d-]+\.)+[a-z]{2,4}.{0,100}"
    lines = re.findall(regex, lines)
    return lines


def getUrlContent(url):
    result = requests.get(
        url,
        headers=_headers_get
    )
    return result.text


def getPastebinEmail(conn):
    if telegram_on:
        mi_bot = telegram.Bot(token=TOKEN)
        mi_bot_updater = Updater(mi_bot.token)

    result = requests.get(
        "https://scrape.pastebin.com/api_scraping.php?limit=250",
        headers=_headers_get
    )
    c = result.json()
    url = ""
    for value in c:
        found_results = False
        ref = value['key']
        url = value['scrape_url']
        #url = "https://pastebin.com/%s" % ref
        #url_raw = "https://pastebin.com/raw%s" % ref
        content = getUrlContent(url)
        lines = searchEmailALine(content)
        emails = searchEmail(content)
        for line in lines:
            line_ = re.sub('\s+', ' ', line).strip()
            email = searchEmail(line_)[0]
            line = urllib.parse.quote(line_)
            #print(email)
            with conn.cursor() as cur:
                exist = cur.execute('select email from pastebin where email = "%s" and ref = "%s" LIMIT 1' % (email,ref))
                if exist==0:
                    found_results = True
                    url = "https://pastebin.com/%s" % ref
                    print("-------")
                    print(url)
                    print(email)
                    if line_!=email:
                        print(line_)
                    cur.execute("insert into pastebin (email, line, ref, url) values('%s', '%s', '%s', '%s')" % (email,line,ref,url))
                    conn.commit()
        if telegram_on and found_results:
            try:
                mi_bot.sendMessage(chat_id=mi_canal, text=("%s" % url))
                mi_bot.sendMessage(chat_id=mi_canal, text=("%s" % str(emails)))
            except Exception as e:
                pass
        time.sleep(1)

def main():
    ascii_banner = pyfiglet.figlet_format("PasteBinWhisper")
    print("\n"+ascii_banner)
    conn = pymysql.connect(host, user=user,port=port,passwd=password, db=dbname)
    while True:
        print(datetime.datetime.now().strftime("%H:%M %d/%m/%y"))
        # Search
        getPastebinEmail(conn)
        time.sleep(time_tag)

if __name__ == "__main__":
    main()
