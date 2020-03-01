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
docker run -it --name bot -v /home/docker/ReinhardtBot/persistent_data:/usr/src/ReinhardtBot/persistent_data -e BOT_TOKEN=<YOUR TOKEN> -e TENOR_API_KEY=<YOUR TENOR API KEY> reinhardtbot:0.1
```

(for production)

```
docker run --name bot -v /home/docker/ReinhardtBot/persistent_data:/usr/src/ReinhardtBot/persistent_data -e BOT_TOKEN=<YOUR TOKEN> -e TENOR_API_KEY=<YOUR TENOR API KEY> --detach reinhardtbot:0.1
```

## Build & Run from Source

TODO

# Documentation

This bot is based on Python 3.8 and implemented according to the [Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md).

## Commands

| /help         | Show Help                                 |
| ------------- | ----------------------------------------- |
| /locations    | All Places                                |
| /wievoll      | Wie voll ist es zu einer bestimmten Zeit? |
| /wievolljetzt | Wie voll ist es jetzt gerade?             |
| /setlocation  | Set your personal location                |
