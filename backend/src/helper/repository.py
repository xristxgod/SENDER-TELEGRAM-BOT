import json
from typing import Optional, Dict, List, Tuple
from datetime import datetime

import aiofiles

from src.helper.types import MessageController, SetMessage
from config import WAIT_TRANSACTION, logger


class MessageRepository(MessageController):
    """
    This class is used to store messages
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MessageRepository, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        """
        {
            "userId": {"network": (timestamp, nodeTransactionId, [{"address": "amount"}], [(support_id, message_id)]), text},
            "123": {"bsc_bip20_usdt": (1653880199, 666, [{"0x7AE2F5B9e386cd1B50A4550696D957cB4900f03a": "14.0000000"}], [(123241, 23)] = text)
        }
        """
        self.__messages: Dict = {}

    async def set_message(self, data: SetMessage, supports_info: List[Tuple[int, int]]) -> Tuple[bool, Optional[str]]:
        try:
            if data.userId in self.__messages.keys():
                if data.network in self.__messages.get(data.userId).keys():
                    logger.error((
                        "THERE HAS ALREADY BEEN A TRANSACTION IN THE REPOSITORY ON THIS NETWORK! IT WILL BE REPLACED!\n"
                        f"TX INFO: {self.__messages.get(data.userId)[data.network]}"
                    ))
                self.__messages.get(data.userId)[data.network] = (
                    int(datetime.timestamp(datetime.now())), data.nodeTransactionId, data.outputs, supports_info
                )
            else:
                self.__messages.update({data.userId: {
                    data.network: (
                        int(datetime.timestamp(datetime.now())), data.nodeTransactionId, data.outputs, supports_info
                    )
                }})
            return True, None
        except Exception as error:
            logger.error(f"ERROR SET MESSAGE: {error}")
            return False, str(error)
        finally:
            if await JSONRepository.set_message(data=data, supports_info=supports_info):
                logger.error("WRITE TO JSON REPOSITORY")

    async def get_message(self, user_id: int, network: str) -> Optional[Dict]:
        if user_id in self.__messages.keys() and network in self.__messages.get(user_id).keys():
            return self.__messages.get(user_id)[network]
        return await JSONRepository.get_message(user_id=str(user_id), network=network)

    async def delete_message(self, user_id: int, network: str) -> Tuple[bool, Optional[str]]:
        try:
            if user_id in self.__messages.keys() and network in self.__messages.get(user_id).keys():
                self.__messages.get(user_id).pop(network)
            if user_id in self.__messages.keys() and len(self.__messages.get(user_id).keys()) == 0:
                self.__messages.pop(user_id)
            return (self.__messages.get(user_id) is None) or (network not in self.__messages.get(user_id).keys()), None
        except Exception as error:
            logger.error(f"ERROR DELETE MESSAGE: {error}")
            return False, str(error)
        finally:
            if await JSONRepository.delete_message(user_id=str(user_id), network=network):
                logger.error("DELETE MESSAGE FROM REPOSITORY")

    # <<<======================================>>> Message <<<=======================================================>>>

    @property
    async def messages(self) -> Dict:
        if len(self.__messages.keys()) == 0:
            return await JSONRepository.messages()
        return self.__messages

    @messages.setter
    def messages(self, message: Dict):
        logger.error("SET NEW TRANSACTIONS DICT")
        self.__messages = message

    @messages.deleter
    def messages(self):
        logger.error("CLEAR ALL TRANSACTIONS")
        self.__messages = {}


class JSONRepository:

    @staticmethod
    async def get() -> Dict:
        async with aiofiles.open(WAIT_TRANSACTION, "r", encoding="utf-8") as file:
            data = await file.read()
        return json.loads(data)

    @staticmethod
    async def set(messages: Dict) -> bool:
        async with aiofiles.open(WAIT_TRANSACTION, "w", encoding="utf-8") as file:
            await file.write(json.dumps(messages))
        return True

    @staticmethod
    async def set_message(data: SetMessage, supports_info: List[Tuple[int, int]]) -> bool:
        messages = await JSONRepository.get()
        user_id = str(data.userId)
        try:
            if user_id in messages.keys():
                if data.network in messages.get(user_id).keys():
                    logger.error((
                        "THERE HAS ALREADY BEEN A TRANSACTION IN THE REPOSITORY ON THIS NETWORK! IT WILL BE REPLACED!\n"
                        f"TX INFO: {messages.get(data.userId)[data.network]}"
                    ))
                messages.get(user_id)[data.network] = (
                    int(datetime.timestamp(datetime.now())), data.nodeTransactionId, data.outputs, supports_info
                )
            else:
                messages.update({user_id: {
                    data.network: (
                        int(datetime.timestamp(datetime.now())), data.nodeTransactionId, data.outputs, supports_info
                    )
                }})
            return await JSONRepository.set(messages)
        except Exception as error:
            logger.error(f"ERROR SET JSON MESSAGE: {error}")
            return False

    @staticmethod
    async def get_message(user_id: str, network: str) -> Optional[Dict]:
        messages = await JSONRepository.get()
        if user_id in messages.keys() and network in messages.get(user_id).keys():
            return messages.get(user_id)[network]
        return None

    @staticmethod
    async def delete_message(user_id: str, network: str) -> bool:
        messages = await JSONRepository.get()
        try:
            if user_id in messages.keys() and network in messages.get(user_id).keys():
                messages.get(user_id).pop(network)
            if user_id in messages.keys() and len(messages.get(user_id).keys()) == 0:
                messages.pop(user_id)
            return await JSONRepository.set(messages)
        except Exception as error:
            logger.error(f"ERROR DELETE JSON MESSAGE: {error}")
            return False

    @staticmethod
    async def messages() -> Dict:
        return await JSONRepository.get()


message_repository = MessageRepository()
