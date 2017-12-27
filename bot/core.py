from telegram import ReplyKeyboardMarkup, KeyboardButton, ParseMode

import re, time, textwrap, feedparser, json, time

import strings
import config

def start(bot, update):
    update.message.reply_text('Hi! I am the bot that fuels the @gamedev_channel!' +
    'GitHub: https://github.com/aBARICHELLO/gamedev_channel_bot')

def parse(bot):
    i = 0
    while i < len(config.WEBSITES):
        d = feedparser.parse(config.WEBSITES[i])
        title = d.entries[0].title
        description = clean_html(str(d.entries[0].description))
        description = textwrap.shorten(description, width=256, placeholder='<i>[...]</i>')

        try:
            url = d.entries[0].url
        except (AttributeError, KeyError):
            url = d.entries[0].link

        published = ''
        try:
            published = d.entries[0].published
        except (AttributeError, KeyError):
            published = d.feed.published

        try:
            with open('json/' + clean_filename(title) + '.txt', 'r') as file:
                old_published = json.load(file)
                if old_published == published: # Repeated entry
                    break
        except FileNotFoundError:
            print('-- NEW ARTICLE --\n' + title)
            bot.send_message(chat_id=config.MAINTANER, # bot.send_message(chat_id=config.NEWS_CHANNEL,
                text='<a href=\"'+ url +'\">'+ title +'</a>'+ '\n' +description,
                parse_mode=ParseMode.HTML)

        with open('json/' + clean_filename(title) + '.txt', 'w') as out: # Save article
            json.dump(published, out)
        i += 1

    print(time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.gmtime()))
    time.sleep(600) # Sleep for 10 mins

def clean_html(description):
    cln = re.compile('<[^>]*>')
    cleaned = re.sub(cln, '', description)
    return cleaned

def clean_filename(filename):
    return filename.strip(' ?;:\\n')

def get_help(bot, update): # Shows a helpful text
    update.message.reply_text(strings.HELP_STRING)
