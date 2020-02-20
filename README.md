# ReinhardtBot

A telegram bot just for shits and giggles.

## Build & Run with Docker

The Dockerfile will automatically set up the environment. 

Build the image with 

```bash
docker image build -t reinhardtbot:0.1 .
```

Start the container with (for debugging)

```
docker run -it --name bot reinhardtbot:0.1
```

(for production)

```
docker run --name bot --detach reinhardtbot:0.1
```

# Documentation

This bot is based on Python 3.8 and implemented according to the [Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md).

## Domain terminology

## Bot Token

If you want to run this bot yourself, you need to connect it to the Telegram API by providing a bot token. You need to create the file `bot_token_provider.py` in the `bot` directory and inside the file implement:

```
class BotTokenProvider:
	token = '<your token here>'
```

That way the bot controller can retrieve the token during runtime and initialized the Telegram Updater.