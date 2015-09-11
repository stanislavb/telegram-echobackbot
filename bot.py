#!/usr/bin/env python3
import argparse
import logging
import time
import json
from api import TelegramAPI


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class TelegramBot:

    def __init__(self, token):
        boturl = 'https://api.telegram.org/bot'
        logger.info('Secret bot URL: {0}{1}/'.format(boturl, token))
        self.api = TelegramAPI(url='{0}{1}/'.format(boturl, token))

        # Make this bot self-aware
        myself = self.api.get_me()
        self.id = myself['id']
        self.first_name = myself['first_name']
        self.username = myself['username']

    def handle_message(self, message):
        if 'left_chat_participant' not in message:
            return json.dumps(message)
        return None

    def respond(self, message):
        chat_id = message['chat']['id']
        returntext = self.handle_message(message)
        if returntext:
            try:
                self.api.send_message(chat_id, text=returntext)
            except:
                logger.exception("Failed to send message.")
        return returntext


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--offset', '-o')
    parser.add_argument('--limit', '-l')
    parser.add_argument('--timeout', '-t')
    parser.add_argument('--wait', '-w')
    parser.add_argument('token')
    args = parser.parse_args()

    bot = TelegramBot(token=args.token)
    offset = args.offset if args.offset else 0
    wait = args.wait if args.wait else 15
    while True:
        logger.info('Waiting {} seconds'.format(wait))
        time.sleep(wait)
        try:
            updates = bot.api.get_updates(
                offset=offset,
                limit=args.limit,
                timeout=args.timeout)
        except:
            logger.exception("Failed to get updates.")
        for update in updates:
            if 'message' in update:
                bot.respond(update['message'])
            if update['update_id'] >= offset:
                offset = update['update_id'] + 1
