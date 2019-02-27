import feedparser
import dataset
import logging
from datetime import datetime, timedelta
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup

import strings
import config


buffer = []
MAX_UPDATES_PER_HOUR = 5
db = dataset.connect(config.PG_LINK, row_type=dict)


def start(bot, update):
    update.message.reply_text(strings.GREETING_TEXT)


def parse(bot, job):
    logging.info('-- Starting buffer')
    start_time = datetime.now()

    with open('websites.txt', 'r') as websites:
        for line in websites:
            page = feedparser.parse(line)

            if line.startswith('#'):  # websites.txt supports comments
                continue

            if len(buffer) >= MAX_UPDATES_PER_HOUR:
                logging.info('Reached max updates per hour')
                break

            if page.status >= 400:
                msg = 'Could not reach feed:\n' + str(page.bozo_exception)
                logging.error(msg)
                report_to_maintainer(bot, msg)
                continue

            feed_title = page.feed.title
            post_title = page.entries[0].title
            url = page.entries[0].link
            logging.info(f'-- Parsing: {feed_title}')

            # Fixes for inconsistent element naming in some RSS feeds
            if 'published' in page.feed:
                published = page.entries[0].published
            else:
                published = page.entries[0].updated

            table = db['feeds']
            if not table.find_one(feed_title=feed_title, post_title=post_title):
                info = {'url': url, 'feed_title': feed_title, 'post_title': post_title}
                buffer.append(info)

                table.insert({
                    'feed_title': feed_title,
                    'post_title': post_title,
                    'url': url,
                    'published': published
                })
                logging.info(f'Buffered {post_title}')

    # Report time taken to buffer
    end_time = datetime.now()
    total_time = (end_time - start_time).total_seconds()
    total_time_str = f'Buffering took {total_time} seconds with {len(buffer)} elements.'
    logging.info(total_time_str)
    report_to_maintainer(bot, total_time_str)

    # Schedule next job according to env GDC_BUFFER
    next_job = config.GDC_BUFFER - total_time
    logging.info(f'-- Next job scheduled to run in {next_job} seconds')
    job.job_queue.run_once(send_messages_from_buffer, when=next_job, name='message_job')


def send_messages_from_buffer(bot, job):
    logging.info('-- Sending messages from buffer')
    for element in buffer:
        send_to_channel(bot, element)
    logging.info('-- Empty buffer')
    buffer.clear()


def send_to_channel(bot, info):
    feed_title = info['feed_title']
    if len(feed_title) > 30:  # Strip long feed titles
        feed_title = feed_title[0:30] + '...'
    keyboard = [
        [InlineKeyboardButton(feed_title, url=info['url'])]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(
        chat_id=config.NEWS_CHANNEL,
        text=f'<a href="{info["url"]}"> {info["post_title"]}</a>',
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )


def print_jobs(bot, update, job):
    update.message.reply_text(str(job.next_job))


def report_to_maintainer(bot, message):
    bot.send_message(chat_id=config.GDC_MAINTAINER, text=message)


def get_help(bot, update):
    update.message.reply_text(strings.HELP_STRING)
