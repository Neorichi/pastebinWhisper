# pastebinWhisper
> Get the newest emails and possible passwords from pastebin (Python3 based)


## Instalation

Install python3 and pip3

<pre> sudo apt install python3 </pre>
<pre> sudo apt install python3-pip</pre>

Install the dependencies via pip:

<pre> pip3 install -r requirements.txt </pre>

#### Important

PasteBin PRO API required (Scraping API is only available for LIFETIME PRO members, and only for those who have their IP whitelisted.)
https://pastebin.com/doc_scraping_api

Change DB Config (mysql)
<pre>
host="xxxx.xxxx.us-east-1.rds.amazonaws.com"
port=3306
dbname="xxxxx"
user="xxxxx"
password="xxxxxx"
</pre>

Add "Example schema table" in your database
<pre>
CREATE TABLE `pastebin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(250),
  `line` varchar(250),
  `url` varchar(250),
  `ref` varchar(45),
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
</pre>

Add Telegram API and Group ID (Optional)
<pre>
telegram_on = True
TOKEN = 'xxxxx:xxxx-xxx'
mi_canal = xxxxxx
</pre>

## Usage
<pre>usage: python3 pastebinWhisper.py  </pre>


## Example
<pre>
python3 pastebinWhisper.py


 ____           _       ____  _    __        ___     _                     
|  _ \ __ _ ___| |_ ___| __ )(_)_ _\ \      / / |__ (_)___ _ __   ___ _ __
| |_) / _` / __| __/ _ \  _ \| | '_ \ \ /\ / /| '_ \| / __| '_ \ / _ \ '__|
|  __/ (_| \__ \ ||  __/ |_) | | | | \ V  V / | | | | \__ \ |_) |  __/ |   
|_|   \__,_|___/\__\___|____/|_|_| |_|\_/\_/  |_| |_|_|___/ .__/ \___|_|   
                                                          |_|              

-------
https://pastebin.com/xxxxxxx
XXXXXX@localhost.loca
XXXXXXX@localhost.localdomain
-------
https://pastebin.com/xxxxxxx
XXXXXXXX@xxxxx.com:xxxxxx
-------
https://pastebin.com/xxxxxxx
XXXXXXXX@xxxxx.com:xxxxxx
-------
https://pastebin.com/xxxxxxx
XXXXXXX@gmail.com
XXXXXXX@gmail.com"}],"paginas":2,"rutaVdm":"1,10,81","indexar":true,"documentoId":"CRI-0000695","mostrar":true,"uniqu
-------
https://pastebin.com/xxxxxxx
XXXXXXXX@tree-xxxx-xxxxx.com
-------
https://pastebin.com/xxxxxxx
XXXXXXXX@gmail.com
XXXXXXXX@gmail.com/25I020T3rw/64545
