import os
import decimal
import logging

import emoji

decimals = decimal.Context()
decimals.prec = 10

tb_token = os.getenv("TB_TOKEN", "5160734992:AAHvy0a1itrW5Tcm24fIylMSxKBYHkK6-R0")
admin_ids = os.getenv("ADMIN_IDS", "688225742").split(",")
api_url = os.getenv('API_URL', 'http://127.0.0.1:8000')

symbol = {
    "add": emoji.emojize(":green_circle:"),
    "dec": emoji.emojize(":red_circle:"),
    "reg": emoji.emojize(":yellow_circle:")
}

logger = logging.getLogger(__name__)
