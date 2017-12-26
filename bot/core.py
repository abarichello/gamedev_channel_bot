from time import time
from telegram import ReplyKeyboardMarkup, KeyboardButton, ParseMode

import textwrap
import feedparser

import strings
import config

def start(bot, update):
    d = feedparser.parse('https://www.gamedev.net/rss/4-gamedevnet-news.xml/')
    title = d.entries[0].title
    description = str(d.entries[0].description.strip())
    description = textwrap.shorten(description, width=256, placeholder='[...]')
    bot.send_message(chat_id=update.message.chat_id,
                    text='<b>' + title + '</b>' + '\n' + description,
                    parse_mode=ParseMode.HTML)

def get_help(bot, update): # Shows a helpful text
    update.message.reply_text(strings.HELP_STRING)
