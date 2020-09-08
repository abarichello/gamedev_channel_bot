FROM python:3.7
LABEL author="artur@barichello.me"

COPY . /gdc
COPY ./sql/feeds.sql /docker-entrypoint-initdb.d/
WORKDIR /gdc
RUN pip install -r requirements.txt

CMD ["python3", "bot/bot.py"]
