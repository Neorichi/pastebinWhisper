# -*- coding: utf-8 -*-
import bs4, requests,re, sys
import pymysql
import datetime
import time
import json
import urllib.parse
import pyfiglet


_headers_get = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}

#Time API restrictions, 60 sec recommended
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

def searchEmail(content):
    regex = r"[\w.%+-]+@(?:[a-z\d-]+\.)+[a-z]{2,4}"
    email = re.findall(regex, str(content))
    return email[0]

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
    result = requests.get(
        "https://scrape.pastebin.com/api_scraping.php?limit=250",
        headers=_headers_get
    )
    c = result.json()
    for value in c:
        ref = value['key']
        url = value['scrape_url']
        content = getUrlContent(url)
        lines = searchEmailALine(content)
        for line in lines:
            line_ = re.sub('\s+', ' ', line).strip()
            email = searchEmail(line_)
            line = urllib.parse.quote(line_)
            with conn.cursor() as cur:
                exist = cur.execute('select email from pastebin where email = "%s" and ref = "%s" LIMIT 1' % (email,ref))
                if exist==0:
                    print("-------")
                    print(url)
                    print(email)
                    if line_!=email:
                        print(line_)
                    cur.execute("insert into pastebin (email, line, ref, url) values('%s', '%s', '%s', '%s')" % (email,line,ref,url))
                    conn.commit()
        #time.sleep(0.5)

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
