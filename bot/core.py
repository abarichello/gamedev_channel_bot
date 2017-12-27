from time import time
from telegram import ReplyKeyboardMarkup, KeyboardButton, ParseMode

import re
import time
import textwrap
import feedparser

import strings
import config

def start(bot, update):
    update.message.reply_text("""Hi! I am the bot that fuels the @gamedev_channel!
    GitHub: https://github.com/aBARICHELLO/gamedev_channel_bot""")

def parse(bot):
    while True:
        i = 0
        while i < len(config.WEBSITES):
            d = feedparser.parse(config.WEBSITES[i])
            title = d.entries[0].title
            description = clean_html(str(d.entries[0].description))
            description = textwrap.shorten(description, width=256, placeholder='<i>[...]</i>')
            url = d.entries[0].link

            bot.send_message(chat_id=config.MAINTANER, # bot.send_message(chat_id=config.NEWS_CHANNEL,
                text='<a href=\"'+ url +'\">'+ title +'</a>'+ '\n' +description,
                parse_mode=ParseMode.HTML)
            i += 1
        time.sleep(3600) # Sleep for an hour

def clean_html(description):
    cln = re.compile('<[^>]*>')
    cleaned = re.sub(cln, '', description)
    return cleaned

def get_help(bot, update): # Shows a helpful text
    update.message.reply_text(strings.HELP_STRING)
