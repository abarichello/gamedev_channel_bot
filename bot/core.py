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
            if d.bozo == 1:
                continue

            title = clean_filename(d.entries[0].title)
            feed_title = clean_filename(d.feed.title)

            if 'link' in d.feed:
                url = d.entries[0].link
            else:
                url = d.entries[0].url

            if 'published' in d.feed:
                published = d.entries[0].published
            else:
                published = d.entries[0].updated

            try:
                with open('json/' + feed_title + '/' + title + '.txt', 'r'):
                    # Feed already exists
                    print(feed_title + '\n' + title + '\n--')
            except FileNotFoundError:  # Create a new file for the feed
                bot.send_message(chat_id=config.NEWS_CHANNEL,  # Send to channel
                                 text='<a href=\"' + url + '\">' +title+ '</a>',
                                 parse_mode=ParseMode.HTML)

            try:
                # Make a new folder for the website feed
                os.makedirs('json/' + feed_title)
                bot.send_message(chat_id=config.MAINTAINER,  # Send to maintainer
                                 text='New feed found: ' + feed_title)
            except FileExistsError:
                pass

            # Save article
            with open('json/' + feed_title + '/' + title + '.txt', 'w') as out:
                    dmp = {'title': title, 'published': published}
                    json.dump(dmp, out, indent=2)

    print(time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.gmtime()))

def clean_filename(filename):  # Removes UNIX prohibited symbols in filename
    prohibited = "\\/"
    for c in prohibited:
        filename = filename.replace(c, '')
    return filename

def get_help(bot, update): # Shows a helpful text
    update.message.reply_text(strings.HELP_STRING)
