FROM python:3.7
RUN pip3 install python-telegram-bot --upgrade
RUN pip3 install requests
WORKDIR /usr/src
RUN git clone https://github.com/ReinhardtJ/ReinhardtBot.git
WORKDIR ReinhardtBot
ENV PYTHONPATH /usr/src/ReinhardtBot
RUN mkdir persistent_data
VOLUME /usr/src/ReinhardtBot/persistent_data
WORKDIR bot
CMD python3 bot_controller.py
