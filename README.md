# Telegram Echo Bot
The purpose of this application is to demonstrate how to use the Telegram Bot API. Documentation available at https://core.telegram.org/bots/api

## How to make it work
Contact BotFather on Telegram (https://telegram.me/botfather) via private message and write the '/newbot' command. BotFather will ask you for a name (anything) and a username (globally unique). In return you will get an API token, looking like this:

```
110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw
```

This token is used to authenticate requests to the bot API.

### Run docker container
Automated build on Docker Hub is available.

```
docker run -i --name echobot stanislavb/telegram-echobackbot 110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw
```

### Build docker image by yourself
Handy instructions are in the Makefile.

```
make build
TOKEN=110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw make run
```

## What the bot does
Every 15 seconds it receives pending messages and replies to the source chat_id with the json content of the received update. This gives you insight into what information the bot can gather.
