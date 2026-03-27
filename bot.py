import sqlite3
import random
import telebot

TOKEN = '123' #your bot token
bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('new.db')
cursor = conn.cursor()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'hello! i IT news bot. print /help and get help for bot')
@bot.message_handler(commands=['news'])
def send_news(message):
    conn = sqlite3.connect('new.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title,link,score FROM new ORDER BY RANDOM() LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    if result:
        title, link, score = result
        bot.reply_to(message,f'*{title}*\n\n{link}\n\n{score}',parse_mode='Markdown')
    else:
        bot.reply_to(message,'news are not')
@bot.message_handler(commands=['top_10'])
def top_10(message):
    conn = sqlite3.connect('new.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title,link,score FROM new ORDER BY CAST(score AS INTEGER) DESC LIMIT !)")
    rows = cursor.fetchall()
    conn.close()
    if rows:
        text ='TOP 10 NEWS FOR RAITING'
        for i, (title,link,score) in enumerate(rows, start = 1):
            text += f'{i}. [{title}]({link})\n {score}\n\n'
        bot.reply_to(message,text,parse_mode = 'Markdown')
    else:
        bot.reply_to(message,'news are not')
@bot.message_handler(commands=['help'])
def Help(message):
    bot.reply_to(message,'/help -- help for commands, /top_10 -- you get top 10 news ,/news -- send randon news')

bot.polling()
