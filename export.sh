#!/bin/sh
# RUN WITH source ./export.sh

export NEWS_CHANNEL=    # ID of the Telegram channel where the messages will get sent.
export DEBUG_CHANNEL=   # Channel/Group ID for DEBUG.
export GDC_MAINTAINER=  # ID of the maintainer to get notified about critical errors.
export PG_LINK=         # DB Link to be used.
export GDC_TOKEN=       # Telegram token.
export GDC_BUFFER=      # Time between start of websites.txt parsing and message sending.
echo Exported config variables.
