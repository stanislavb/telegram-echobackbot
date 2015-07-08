#!/usr/bin/env python3
import argparse
import json
import logging
import time
from api import API


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
boturl = 'https://api.telegram.org/bot'


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--offset', '-o')
    parser.add_argument('--limit', '-l')
    parser.add_argument('--timeout', '-t')
    parser.add_argument('--wait', '-w')
    parser.add_argument('token')
    args = parser.parse_args()

    logger.info('Secret bot URL: {0}{1}/'.format(boturl, args.token))
    api = API(url='{0}{1}/'.format(boturl, args.token))

    offset = args.offset if args.offset else 0
    wait = args.wait if args.wait else 15
    while True:
        logger.info('Waiting {} seconds'.format(wait))
        time.sleep(wait)
        updates = api.get_updates(
            offset=offset,
            limit=args.limit,
            timeout=args.timeout)
        for update in updates:
            if 'message' in update:
                message = update['message']
                chat_id = message['chat']['id']
                # Maybe we got kicked out of the channel
                if not 'left_chat_participant' in message:
                    api.send_message(chat_id, json.dumps(message))
            if update['update_id'] >= offset:
                offset = update['update_id'] + 1
