import os
import decimal
import logging

decimals = decimal.Context()
decimals.prec = 10

logger = logging.getLogger(__name__)


class Config:

    USER_BOT_TOKEN = os.getenv("TB_TOKEN")
    USER_BOT_ADMIN_IDS = os.getenv("ADMIN_IDS").split(",")

    P2P_TOKEN = os.getenv("P2P_TB_TOKEN")
    P2P_ADMIN_IDS = os.getenv("P2P_ADMIN_IDS").split(",")

    BOT_APPROVED_TOKEN = os.getenv("APPROVED_TB_TOKEN")
    SUPPORT_ID = int(os.getenv("SUPPORT_ID"))

    APPROVED_DOMAIN = os.getenv("APPROVED_DOMAIN")
    APPROVED_AUTH_BEARER_TOKEN = os.getenv("APPROVED_AUTH_BEARER_TOKEN")

    API_URL = os.getenv("API_URL")
