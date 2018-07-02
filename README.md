# gamedev_channel_bot

<img src="https://i.imgur.com/ZrkbgC8.png" align="right" width="256" height="256">
GameDev channel on Telegram, updated hourly with the best gamedev websites content.

# Channel
[CLICK HERE](http://t.me/gamedev_channel) to join the channel on telegram. The bot checks the websites for new posts every hour.

# Bot
This bot can be repurposed to parse any type of RSS feeds you want, just modify the `websites.txt` file and environment variables in `config.py`.

# Timing
This bot was designed to collect new RSS posts from the last hour and post them together at the minute 0, to prevent the updates from flooding your Telegram and to group them at nice hourly updates.<br>
To accomplish that there are two `python-telegram-bot`'s jobs. The first job is the parse_job, it runs minutes prior (currently 3) to buffer the new entries.<br>
The message_job is scheduled after the parse, it runs after it. This delay is governed by the env var GDC_BUFFER.<br>
Current settings are minute 57 for the parse job and 3 minutes (GDC_BUFFER=180) for the message_job.<br>

# Contributing
To include new RSS feeds to the channel open a pull request and edit the `bot/websites.txt` file located in the repository.
At the Pull Request description include examples of great material that the site has produced and why it is a great gamedev resource.
