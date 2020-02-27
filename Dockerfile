FROM python:3.7

WORKDIR /usr/src
RUN pip3 install python-telegram-bot --upgrade
RUN pip3 install requests
RUN git pull https://github.com/ReinhardtJ/ReinhardtBot.git
ENV PYTHONPATH /usr/src/ReinhardtBot
WORKDIR ReinhardtBot
VOLUME /persistent_data
WORKDIR bot
CMD python3 bot_controller.py