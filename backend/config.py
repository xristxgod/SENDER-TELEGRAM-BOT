import os
import decimal
import logging

import emoji

decimals = decimal.Context()
decimals.prec = 10

tb_token = os.getenv("TB_TOKEN")
admin_ids = os.getenv("ADMIN_IDS").split(",")

p2p_tb_token = os.getenv("P2P_TB_TOKEN")
p2p_admin_ids = os.getenv("P2P_ADMIN_IDS").split(",")

symbol = {
    "add": emoji.emojize(":green_circle:"),
    "dec": emoji.emojize(":red_circle:"),
    "reg": emoji.emojize(":yellow_circle:"),
    "ver": emoji.emojize(":ok_hand:", language='alias')
}

api_url = os.getenv("API_URL")

logger = logging.getLogger(__name__)
