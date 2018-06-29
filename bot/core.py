import feedparser
import dataset
import datetime
import logging
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup

import strings
import config


db = dataset.connect(config.PG_LINK, row_type=dict)
buffer = []

def start(bot, update):
    update.message.reply_text(strings.GREETING_TEXT)


def parse(bot, job):
    start_time = datetime.datetime.now()
    with open('websites.txt', 'r') as websites:
        for line in websites:
            page = feedparser.parse(line)
            if page.bozo == 1:
                report_to_maintainer(bot, f'RSS Error: {line}\n {page.bozo_exception}')
                continue

            feed_title = page.feed.title
            title = page.entries[0].title

            if 'link' in page.feed:
                url = page.entries[0].link
            else:
                url = page.entries[0].url

            if 'published' in page.feed:
                published = page.entries[0].published
            else:
                published = page.entries[0].updated

            table = db[feed_title]
            if not table.find_one(title=title):
                info = {'url': url, 'feed_title': feed_title, 'title': title}
                buffer.append(info)

                table.insert(dict(title=title, date=published, url=url,
                                  added=datetime.datetime.now().isoformat()))
            else:
                print(f' ==> {feed_title}\n - {title} ✔\n')

    end_time = datetime.datetime.now()
    total_time_str = f'Total time: {end_time - start_time}'
    logging.info(total_time_str)
    bot.send_message(chat_id=config.GDC_MAINTAINER,
                     text=total_time_str)


def send_from_buffer(bot, job):
    for element in buffer:
        send_to_channel(bot, element)
    buffer.clear()


def send_to_channel(bot, info):
    feed_title = info['feed_title']
    if len(feed_title) > 30:
        feed_title = feed_title[0:30] + '...'
    keyboard = [
        [InlineKeyboardButton(feed_title, url=info['url'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(
        chat_id=config.NEWS_CHANNEL,
        text=f'<a href="{info["url"]}"> {info["title"]}</a>',
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup)


def report_to_maintainer(bot, message):
    bot.send_message(chat_id=config.GDC_MAINTAINER, text=message)


def get_help(bot, update):
    update.message.reply_text(strings.HELP_STRING)
