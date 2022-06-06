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

tb_approval_token = os.getenv("TB_APPROVAL_TOKEN")
tb_approval_ids = os.getenv("TB_APPROVAL_IDS").split(",")
tb_approval_bearer = os.getenv("TB_APPROVAL_BEARER")
url_approved = os.getenv("URL_APPROVED")

symbol = {
    "add": emoji.emojize(":green_circle:"),
    "dec": emoji.emojize(":red_circle:"),
    "reg": emoji.emojize(":yellow_circle:"),
    "ver": emoji.emojize(":ok_hand:", language='alias'),
    "approved": emoji.emojize(":check_mark_button:"),
    "rejected": emoji.emojize(":cross_mark_button:"),
    "transaction": emoji.emojize(":money_with_wings:")
}

api_url = os.getenv("API_URL")

logger = logging.getLogger(__name__)
