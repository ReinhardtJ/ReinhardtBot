# ReinhardtBot

A telegram bot that can
- Tell you how full your gym is, right now or at any other time! (see below)
- Hide you message from chats with the `spoiler` command!
- Give you a gif-Keyboard from Tenor with the `gif` command!

## Build & Run with Docker

The Dockerfile will automatically set up the environment. 

Build the image with 

```bash
docker image build -t reinhardtbot:0.1 .
```

Start the container with (for debugging)

```
docker run -it --name bot -v /home/docker/ReinhardtBot/persistent_data:/usr/src/ReinhardtBot/persistent_data -e BOT_TOKEN=<YOUR TOKEN> -e TENOR_API_KEY=<YOUR TENOR API KEY> reinhardtbot:0.1
```

(for production)

```
docker run --name bot -v /home/docker/ReinhardtBot/persistent_data:/usr/src/ReinhardtBot/persistent_data -e BOT_TOKEN=<YOUR TOKEN> -e TENOR_API_KEY=<YOUR TENOR API KEY> --detach reinhardtbot:0.1
```

# Documentation

This bot is based on Python 3.8 and implemented according to the [Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md).

## Commands

| /help         | Show Help                                 |
| ------------- | ----------------------------------------- |
| /locations    | All Places                                |
| /wievoll      | How full is my gym currently?             |
| /wievolljetzt | How full is it right now at your gym?     |
| /setlocation  | Set the location of your gym              |
