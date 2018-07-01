import feedparser
import dataset
import logging
from datetime import datetime, timedelta
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup

import strings
import config


buffer = []
db = dataset.connect(config.PG_LINK, row_type=dict)

def start(bot, update):
    update.message.reply_text(strings.GREETING_TEXT)


def parse(bot, job):
    logging.info("Starting buffer")
    start_time = datetime.now()

    with open('websites.txt', 'r') as websites:
        for line in websites:
            page = feedparser.parse(line)

            if line.startswith('#'):
                logging.info(f'Skipped: {line}')
                continue

            if page.bozo == 1:
                message = f'RSS Error: {line}\n {page.bozo_exception}'
                logging.error(message)
                report_to_maintainer(bot, message)
                continue

            feed_title = page.feed.title
            title = page.entries[0].title
            url = page.entries[0].link

            if 'published' in page.feed:
                published = page.entries[0].published
            else:
                published = page.entries[0].updated

            table = db[feed_title]
            if not table.find_one(title=title):
                info = {'url': url, 'feed_title': feed_title, 'title': title}
                buffer.append(info)

                table.insert(dict(title=title, date=published, url=url,
                                  added=datetime.now().isoformat()))
            else:
                print(f' ==> {feed_title}\n - {title} ✔\n')

    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()
    total_time_str = f'Parsing took {total_time} seconds, buffer has {len(buffer)} elements.'
    logging.info(total_time_str)
    bot.send_message(chat_id=config.GDC_MAINTAINER, text=total_time_str)

    next_job = config.GDC_BUFFER - total_time
    logging.info(f'Next job to be scheduled in {next_job} seconds')
    job.job_queue.run_once(send_messages, when=next_job, name='send_to_channel_job')


def send_messages(bot, job):
    logging.info('Sending messages from buffer')
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
