import os
import decimal
import logging

import emoji

decimals = decimal.Context()
decimals.prec = 10

tb_token = os.getenv("TB_TOKEN", "...")
admin_ids = os.getenv("ADMIN_IDS", "...").split(",")

symbol = {
    "add": emoji.emojize(":green_circle:"),
    "dec": emoji.emojize(":red_circle:"),
    "reg": emoji.emojize(":yellow_circle:"),
    "ver": emoji.emojize(":ok_hand:", language='alias')
}

api_url = os.getenv("API_URL", "http://127.0.0.1:8000")

logger = logging.getLogger(__name__)