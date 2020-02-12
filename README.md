# ReinhardtBot

A telegram bot just for shits and giggles. This readme will one day be useful.

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
docker run --name bot reinhardtbot:0.1
```

