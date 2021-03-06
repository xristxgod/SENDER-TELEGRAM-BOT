import json
from typing import Optional, List, Dict, Tuple

import aiohttp

from src.helper.types import SetMessage
from config import Config, logger


class Sender:
    @staticmethod
    async def send_to_bot(text: str, tb_token: str, admin_ids: List[int]):
        try:
            async with aiohttp.ClientSession() as session:
                for user_id in admin_ids:
                    async with session.get(
                            f"https://api.telegram.org/bot{tb_token}/sendMessage",
                            params={
                                "chat_id": user_id,
                                "text": text,
                                "parse_mode": "html"
                            }
                    ) as response:
                        logger.error(f"SEND ({user_id}): {response.ok}")
            logger.error(f'MESSAGE HAS BEEN SENT: {text}.')
            return True
        except Exception as error:
            logger.error(f"ERROR SEND TO BOT: {error}")
            return False

    @staticmethod
    async def send_to_support(
            text: str, tb_token: str, support_ids: List[int], buttons: List[Dict] = None
    ) -> Optional[List[Tuple[int, int]]]:
        try:
            message_ids = []
            async with aiohttp.ClientSession() as session:
                for support_id in support_ids:
                    async with session.get(
                            f"https://api.telegram.org/bot{tb_token}/sendMessage",
                            params={
                                "chat_id": support_id,
                                "text": text,
                                "parse_mode": "html",
                                "reply_markup": json.dumps({
                                    "inline_keyboard": [buttons]
                                })
                            }
                    ) as response:
                        result = (await response.json()).get('result')
                        if result is not None:
                            message_ids.append((
                                support_id, result.get('message_id')
                            ))
                            logger.error(f"SEND ({support_id}): {response.ok}")
            return message_ids
        except Exception as error:
            logger.error(f"ERROR SEND TO BOT: {error}")
            return None

    @staticmethod
    async def edit_message(support_info: List[Tuple[int, int]], text: str, tb_token: str) -> bool:
        try:
            async with aiohttp.ClientSession() as session:
                for message in support_info:
                    async with session.get(
                            f"https://api.telegram.org/bot{tb_token}/editMessageText",
                            params={
                                "chat_id": message[0],
                                "text": text,
                                "parse_mode": "html",
                                "message_id": message[1]
                            }
                    ) as response:
                        logger.error(f"SEND ({message[0]}): {response.ok}")
            return True
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return False


class SenderToSite:
    URL_APPROVED = Config.APPROVED_DOMAIN + "/api/admin/approved"
    URL_REJECT = Config.APPROVED_DOMAIN + "/api/admin/reject"

    __BEARER_TOKEN = Config.APPROVED_AUTH_BEARER_TOKEN

    @staticmethod
    def __get_headers() -> Dict:
        return {"Authorization": SenderToSite.__BEARER_TOKEN}

    @staticmethod
    async def send_to_site(body: SetMessage, status: bool = True) -> bool:
        try:
            async with aiohttp.ClientSession(headers=SenderToSite.__get_headers()) as session:
                async with session.put(
                        url=SenderToSite.URL_APPROVED if status else SenderToSite.URL_REJECT,
                        json={
                            "userId": body.userId,
                            "nodeTransactionId": body.nodeTransactionId,
                            "network": body.network,
                            "outputs": list(body.outputs)
                        }
                ) as response:
                    logger.error(f"SEND TO SITE: {response.ok}")
            return True
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return False
