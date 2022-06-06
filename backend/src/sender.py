import aiohttp
from config import logger


async def send_to_bot(text: str, tb_token, admin_ids):
    """
    Send a message to the telegram bot
    :param text: Message text
    :return: The status of the completed work
    """
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


async def send_to_url_put(url, auth: str, **data):
    try:
        async with aiohttp.ClientSession(headers={
            "Authorization": auth
        }) as session:
            async with session.put(url, json=data) as response:
                logger.error(f"SEND TO APPROVAL | STATUS: {response.ok} ")
                return response
    except Exception as error:
        logger.error(f"ERROR: {error}")
        raise Exception(f"NOT SEND TO APPROVAL")
