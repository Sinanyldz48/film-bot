# -*- coding: utf-8 -*-
"""
Created on Thu May 23 14:57:40 2024

@author: xsina
"""
import logging
import requests
from bs4 import BeautifulSoup
import telegram
from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import time as t
from googletrans import Translator
import random
import schedule
from datetime import datetime
from translate import Translator
translator= Translator(to_lang="Turkish")


cookies = {
    'session-id': '143-1825015-5836529',
    'session-id-time': '2082787201l',
    'csm-hit': 'tb:s-5VQN0N5RBNRVT5SYYPBV|1716465404863&t:1716465405108&adb:adblk_no',
    'ubid-main': '133-8266708-7425634',
    'ad-oo': '0',
    'ci': 'eyJwdXJwb3NlcyI6W10sInZlbmRvcnMiOltdfQ',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
    'cache-control': 'max-age=0',
    # 'cookie': 'session-id=143-1825015-5836529; session-id-time=2082787201l; csm-hit=tb:s-5VQN0N5RBNRVT5SYYPBV|1716465404863&t:1716465405108&adb:adblk_no; ubid-main=133-8266708-7425634; ad-oo=0; ci=eyJwdXJwb3NlcyI6W10sInZlbmRvcnMiOltdfQ',
    'priority': 'u=0, i',
    'referer': 'https://www.google.com/',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}
base_url = "https://www.imdb.com/"
response = requests.get(base_url, cookies=cookies, headers=headers)
print(response.status_code)
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def news():
    url  ="news/top/?ref_=hm_nw_sm"
    response = requests.get(base_url + url, cookies=cookies, headers=headers)
    source = BeautifulSoup(response.content, "html.parser")
    main = source.find("div",attrs={"class":"sc-9bb6373f-0 iWnIEL"})
    items = main.find_all("div",attrs={"data-testid":"item-id"})
    news_list = []
    for i in range(5):
        item = items[i]
        title = item.find("a",attrs={"class":"ipc-link ipc-link--base sc-bec740f7-3 egwFBY"}).text
        description = item.find("div",attrs={"class":"ipc-html-content-inner-div"}).text.split("...")[0]
        tarih = item.find("ul",attrs={"class":"ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline sc-bec740f7-14 gDNDdY base"}).text.split("by")[0]
        link = item.find("a",attrs={"class":"ipc-link ipc-link--base sc-bec740f7-3 egwFBY"})["href"]
        news_list.append({"title": title, "date": tarih, "link": link})
    return news_list
    
def most_populer_movies():
    url = "chart/moviemeter/?ref_=nv_mv_mpm"
    response = requests.get(base_url + url, cookies=cookies, headers=headers)
    source = BeautifulSoup(response.content, "html.parser")
    items = source.find_all("li", attrs={"class": "ipc-metadata-list-summary-item sc-10233bc-0 iherUv cli-parent"})
    title = ""
    movie_list = []
    for i in range(10):  # İlk 10 öğeyi al
        item = items[i]  # Listenin i. öğesini al
        link = base_url + item.find("a",attrs={"class":"ipc-title-link-wrapper"})["href"]
        title = item.find("h3").text.strip()
        imdb = item.find("span", attrs={"data-testid": "ratingGroup--imdb-rating"}).text.split('\xa0')[0]
        row = item.find("div", attrs={"class": "sc-b189961a-7 feoqjK cli-title-metadata"}).text.strip()
        year = row[:4]
        length = row[4:9].replace(" ", "").replace("h", ":")
        movie_list.append({"title": title, "imdb": imdb, "year": year, "length": length, "link":link})
    return movie_list
            
            
def top_10_movie():
    url = "chart/top/?ref_=nv_mv_250"
    response = requests.get(base_url + url, cookies=cookies, headers=headers)
    source = BeautifulSoup(response.content, "html.parser")
    items = source.find_all("li", attrs={"class": "ipc-metadata-list-summary-item"})
    title = ""
    movie_list = []
    for i in range(10):  # İlk 10 öğeyi al
        item = items[i]  # Listenin i. öğesini al
        link = base_url + item.find("a",attrs={"class":"ipc-title-link-wrapper"})["href"]
        title = item.find("h3").text.strip()
        imdb = item.find("span", attrs={"data-testid": "ratingGroup--imdb-rating"}).text.split('\xa0')[0]
        row = item.find("div", attrs={"class": "sc-b189961a-7 feoqjK cli-title-metadata"}).text.strip()
        year = row[:4]
        length = row[4:9].replace(" ", "").replace("h", ":")
        movie_list.append({"title": title, "imdb": imdb, "year": year, "length": length, "link": link})
    return movie_list
#########


def get_random_movie(a=random.randint(1, 100)):
    base_url = "https://www.imdb.com/"
    url = "chart/top/?ref_=nv_mv_250"
    response = requests.get(base_url + url, headers=headers)
    source = BeautifulSoup(response.content, "html.parser")
    items = source.find_all("li", attrs={"class": "ipc-metadata-list-summary-item"})
    movie_list = []
    link_list = []
    for i in range(a,a+1):
        print(i)
        item = items[i]
        link = base_url + item.find("a")["href"]
        link_list.append(link)
        response = requests.get(link, headers=headers)
        source = BeautifulSoup(response.content, "html.parser")
        aciklama_element = source.find("span", attrs={"class": "sc-7193fc79-1 jgFQCx"})
        if aciklama_element is not None:
            aciklama = aciklama_element.text
        else:
            print("Açıklama bulunamadı, film atlandı.")
            continue
        
        div_element = source.find("div", attrs={"class": "sc-b7c53eda-0 dUpRPQ"})
        title_element = div_element.find("h1")
        if title_element is not None:
            title_text = title_element.text
        else:
            print("Başlık bulunamadı, film atlandı.")
            continue
        
        div_desc = div_element.find("div")
        if div_desc is not None:
            desc_parts = div_desc.text.split(":")
            if len(desc_parts) > 1:
                desc = desc_parts[1]
            else:
                print("Açıklama parçası bulunamadı, film atlandı.")
                continue
        else:
            print("Açıklama bulunamadı, film atlandı.")
            continue
        
        title = title_text + "(" + desc + ")"
        
        year = div_element.find("ul").text[:4]
        length = div_element.find("ul").text[7:]
        imdb = source.find("span", attrs={"class": "sc-bde20123-1 cMEQkK"}).text
        div_tur = source.find("div", attrs={"class": "ipc-chip-list__scroller"})
        tur_a = div_tur.find_all("a")
        tur = ""
        for item in tur_a:
            tur += item.find("span").text + ","
        tur = tur.rstrip(",")
        movie_list.append({
            "title": title,
            "year": year,
            "length": length,
            "imdb": imdb,
            "tur": tur,
            "aciklama": aciklama,
            "link": link
        })
    random_movie = random.choice(movie_list)  # Rastgele bir filmi seç
    return random_movie

######## Ana Menü
keyboard = [
    [
        InlineKeyboardButton("\U0001F51D IMDB En Yüksek 10", callback_data='1'),
        InlineKeyboardButton("\U0001F525 Trendler ilk 10", callback_data='2'),
    ],
    [   InlineKeyboardButton("\U0001F4FA Ekran Gündemi", callback_data='3'),
        InlineKeyboardButton("\U0001F39E Rastgele Film", callback_data='4'),
    ],
    [InlineKeyboardButton("\U0001F3A5 Kategoriye Göre Rastgele Filmler", callback_data='5')]
]
reply_markup = InlineKeyboardMarkup(keyboard)
########
###### Kategoriler Menüsü
keyboard_category = [
    [
        InlineKeyboardButton("\U0001F4A5 Aksiyon", callback_data='6'),
        InlineKeyboardButton("\U0001F304 Macera", callback_data='7'),
    ],
    [   InlineKeyboardButton("\U0001F308 Animasyon", callback_data='8'),
        InlineKeyboardButton("\U0001F3AD Dram", callback_data='9'),
    ],
    [    InlineKeyboardButton("\U00002694 Savas", callback_data='10'),
        InlineKeyboardButton("\U0001F47B Korku", callback_data='11'),
    ],
    [   
        InlineKeyboardButton("Ana Menü", callback_data='main_menu')
    ]
]
reply_markup2 = InlineKeyboardMarkup(keyboard_category)
######
def start(update: Update, context: CallbackContext) -> None:
    user_first_name = update.message.from_user.first_name
    # Kullanıcı adını yazdır
    update.message.reply_text(f'\U0001F973  Merhaba, {user_first_name} Hoşgeldin  \U0001F973')
    t.sleep(1)
    update.message.reply_text('Yardımcı Olabileceğim Seçimler:\U0001F4CC', reply_markup=reply_markup)
    
#Global değişkenler daha hızlı yuklenmesi için burda tanımlandı
user_id=0
BOT_TOKEN = "7093014029:AAG6OgYYrwPWEVOVE3hyI9N8QWQqJZ4P70o" 
global movie_list
movie_list = top_10_movie()
movie_list2 = most_populer_movies()
new_list = news()
bot = telegram.Bot(token=BOT_TOKEN)
random_movie = get_random_movie()


def category_film(category_name):
    url  ="search/title/?genres="+ category_name + "&explore=genres"
    response = requests.get(base_url + url, cookies=cookies, headers=headers)
    source = BeautifulSoup(response.content, "html.parser")
    main = source.find("ul",attrs={"class":"ipc-metadata-list ipc-metadata-list--dividers-between sc-748571c8-0 jmWPOZ detailed-list-view ipc-metadata-list--base"})
    items = main.find_all("li")
    category_move_list =[]
    for i in range(50):
        item = items[i]
        link = base_url + item.find("a",attrs={"class":"ipc-title-link-wrapper"})["href"]
        title = item.find("h3").text
        div_element = item.find("div",attrs={"class":"sc-b189961a-7 feoqjK dli-title-metadata"})
        year = div_element.text[:4]
        imdb_element = item.find("div",attrs={"class":"sc-e2dbc1a3-0 ajrIH sc-b189961a-2 fkPBP dli-ratings-container"})
        if imdb_element.text != "":
            imdb = imdb_element.text.split("(")[0].strip()
        else:
            imdb = "Puan Henüz Girilmemiş"
        aciklama = item.find("div",attrs={"class":"ipc-html-content-inner-div"}).text

        print(title)
        category_move_list.append({"title":title,"link":link,"year":year,"imdb":imdb,"aciklama":aciklama})
    random_5_movies = random.sample(category_move_list, 5)
    return random_5_movies

def mesaj_gonder_category(liste,chat_id):
    for movie in liste:
        caption = (
            f"<a href='{movie['link']}'><b>{movie['title']}</b></a>\n"
            f"{movie['aciklama']}\n\n"
            f"Yıl: {movie['year']}\n\n"
            f"IMDB: {movie['imdb']}\n\n"
            ) 
        bot.sendMessage(chat_id = chat_id, text = caption, 
                         parse_mode = telegram.ParseMode.HTML, 
                         disable_web_page_preview = False)  

def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    chat_id = update.effective_chat.id
    if query.data == "1":
        global movie_list
        for movie in movie_list:
            caption = f"<a href='{movie['link']}'><b>{movie['title']}</b></a>\nIMDb: {movie['imdb']}\nYayınlanma Yılı: {movie['year']}\nFilm Uzunluğu: {movie['length']}"
            bot.sendMessage(chat_id = chat_id, text = caption, 
                             parse_mode = telegram.ParseMode.HTML, 
                             disable_web_page_preview = False)
    elif query.data == "2":
        global movie_list2
        for movie in movie_list2:
            caption = f"<a href='{movie['link']}'><b>{movie['title']}</b></a>\n\nIMDb: {movie['imdb']}\nYayınlanma Yılı: {movie['year']}\nFilm Uzunluğu: {movie['length']}"
            bot.sendMessage(chat_id = chat_id, text = caption, 
                             parse_mode = telegram.ParseMode.HTML, 
                             disable_web_page_preview = False)  
    elif query.data == "3":
        for new in new_list:
            caption = f"<b>{new['title']}</b>\n{new['date']}\nLink: {new['link']}"
            bot.sendMessage(chat_id = chat_id, text = caption, 
                             parse_mode = telegram.ParseMode.HTML, 
                             disable_web_page_preview = False)  
    elif query.data == "4":
        global random_movie
        caption = (
            f"<a href='{random_movie['link']}'><b>{random_movie['title']}</b></a>\n"
            f"{random_movie['aciklama']}\n\n"
            f"Tür: {random_movie['tur']}\n\n"
            f"Yıl: {random_movie['year']}\n\n"
            f"IMDB: {random_movie['imdb']}\n\n"
            f"Süre: {random_movie['length']}\n\n" 
            ) 
        bot.sendMessage(chat_id = chat_id, text = caption, 
                             parse_mode = telegram.ParseMode.HTML, 
                             disable_web_page_preview = False)  
        random_sayi = random.randint(1, 100)
        random_movie = get_random_movie(random_sayi) 
    elif query.data == "5":
        try:
            query.edit_message_text(text="Kategoriler", reply_markup=reply_markup2)

        except Exception as e:
            logger.error(f"Hata oluştu: {e}")
    elif query.data == "6":
        movieList = category_film("action")
        mesaj_gonder_category(movieList, chat_id)
        t.sleep(2)
        query.edit_message_text(text='Yardımcı Olabileceğim Seçimler:\U0001F4CC', reply_markup=reply_markup)
        
    elif query.data == "7":
        movieList = category_film("adventure")
        mesaj_gonder_category(movieList, chat_id)
    elif query.data == "8":
        movieList = category_film("animation")
        mesaj_gonder_category(movieList, chat_id)
    elif query.data == "9":
        movieList = category_film("drama")
        mesaj_gonder_category(movieList, chat_id)
    elif query.data == "10":
        movieList = category_film("war")
        mesaj_gonder_category(movieList, chat_id)
    elif query.data == "11":
        movieList = category_film("horror")
        mesaj_gonder_category(movieList, chat_id)
    elif query.data == "main_menu":
        try:
            query.edit_message_text(text='Yardımcı Olabileceğim Seçimler:\U0001F4CC', reply_markup=reply_markup)

        except Exception as e:
            logger.error(f"Hata oluştu: {e}")
        
    #query.edit_message_text(text='Yardımcı Olabileceğim Seçimler:\U0001F4CC', reply_markup=reply_markup)
    
def menu(update: Update, context: CallbackContext) -> None:
    """Menü Kısmı"""
    update.message.reply_text(text='Yardımcı Olabileceğim Seçimler:\U0001F4CC', reply_markup=reply_markup)


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('menu', menu))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()


