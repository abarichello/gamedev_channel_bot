import feedparser, json, os, time
from telegram import ParseMode

import strings
import config

def start(bot, update):
    update.message.reply_text(strings.GREETING_TEXT)

def parse(bot, job):
    with open('websites.txt', 'r') as websites:
        for line in websites:
            d = feedparser.parse(line)
            title = clean_filename(d.entries[0].title)
            feed_title = clean_filename(d.feed.title)

            try:
                url = d.entries[0].url
            except (AttributeError, KeyError):
                url = d.entries[0].link

            published = d.entries[0].published

            try:
                with open('json/' + feed_title + '/' + title + '.txt', 'r'):
                    print(feed_title + '\n' + title + '\n--')  # Feed already exists
            except FileNotFoundError:  # Create a new file for the feed
                bot.send_message(chat_id=config.DEBUG_CHANNEL,
                                 text='New feed: ' + feed_title + '\n' + title)

                bot.send_message(chat_id=config.NEWS_CHANNEL,
                                 text='<a href=\"' + url + '\">' +title+ '</a>',
                                 parse_mode=ParseMode.HTML)
            
                try:
                    os.makedirs('json/' + feed_title)  # Make a new folder for the website feed
                except FileExistsError:
                    pass

            with open('json/' + feed_title + '/' + title + '.txt', 'w') as out:  # Save article
                    dmp = {'title': title, 'published': published}
                    json.dump(dmp, out, indent=2)
    print(time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.gmtime()))

def clean_filename(filename):  # Removes prohibited symbols in filename
    return filename.strip('  ?;:\\n')

def get_help(bot, update): # Shows a helpful text
    update.message.reply_text(strings.HELP_STRING)
