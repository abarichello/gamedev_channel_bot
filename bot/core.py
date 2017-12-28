import re, textwrap, feedparser, json, os
from telegram import ParseMode

import strings
import config

def start(bot, update):
    update.message.reply_text(strings.GREETING_TEXT)

def parse(bot):
    with open('websites.txt', 'r') as websites:
        for line in websites:
            d = feedparser.parse(line)
            title = clean_filename(d.entries[0].title)
            feed_title = clean_filename(d.feed.title)
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
                with open('json/' + feed_title + '/' + title + '.txt', 'a+'):
                    pass  # Feed already exists
            except FileNotFoundError:  # Create a new file for the feed
                bot.send_message(chat_id=config.NEWS_CHANNEL,
                                text='<a href=\"' + url + '\">' + title + '</a>' + '\n' + description,
                                parse_mode=ParseMode.HTML)

                os.makedirs('json/' + feed_title)  # Make a new folder for the website feed
                with open('json/' + feed_title + '/' + title + '.txt', 'w') as out:  # Save article
                    dmp = {'title': title, 'published': published}
                    json.dump(dmp, out, indent=2)

def clean_html(description):
    cln = re.compile('<[^>]*>') # Remove HTML tags
    cleaned = re.sub(cln, '', description)
    return cleaned.replace('\"', '')

def clean_filename(filename):
    return filename.strip('  ?;:\\n')

def get_help(bot, update): # Shows a helpful text
    update.message.reply_text(strings.HELP_STRING)
