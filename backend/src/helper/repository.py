from typing import Optional, Dict, Tuple
from datetime import datetime

from src.helper.types import MessageController, SetMessage
from config import logger


class MessageRepository(MessageController):
    """
    This class is used to store messages
    """
    def __init__(self):
        """
        {
            "userId": {"network": (timestamp, nodeTransactionId, [{"address": "amount"}])},
            "123": {"bsc_bip20_usdt": (1653880199, 666, [{"0x7AE2F5B9e386cd1B50A4550696D957cB4900f03a": "14.0000000"}])
        }
        """
        self.__messages: Dict = {}

    def set_message(self, data: SetMessage) -> Tuple[bool, Optional[str]]:
        try:
            if data.userId in self.__messages.keys():
                if data.network in self.__messages.get(data.userId).keys():
                    logger.error((
                        "THERE HAS ALREADY BEEN A TRANSACTION IN THE REPOSITORY ON THIS NETWORK! IT WILL BE REPLACED!\n"
                        f"TX INFO: {self.__messages.get(data.userId)[data.network]}"
                    ))
                self.__messages.get(data.userId)[data.network] = (
                    datetime.timestamp(datetime.now()), data.nodeTransactionId, data.outputs
                )
            else:
                self.__messages.update({data.userId: {
                    data.network: (datetime.timestamp(datetime.now()), data.nodeTransactionId, data.outputs)
                }})
            return True, None
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return False, str(error)

    def get_message(self, user_id: int, network: str) -> Optional[Dict]:
        if user_id in self.__messages.keys() and network in self.__messages.get(user_id).keys():
            return self.__messages.get(user_id)[network]
        return None

    def delete_message(self, user_id: int, network: str) -> Tuple[bool, Optional[str]]:
        try:
            if user_id in self.__messages.keys() and network in self.__messages.get(user_id).keys():
                self.__messages.get(user_id).pop(network)
            if len(self.__messages.get(user_id).keys()) == 0:
                self.__messages.pop(user_id)
            return (self.__messages.get(user_id) is None) or (network not in self.__messages.get(user_id).keys()), None
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return False, str(error)

    # <<<======================================>>> Message <<<=======================================================>>>

    @property
    def messages(self) -> Dict:
        return self.__messages

    @messages.setter
    def messages(self, message: Dict):
        logger.error("SET NEW TRANSACTIONS DICT")
        self.__messages = message

    @messages.deleter
    def messages(self):
        logger.error("CLEAR ALL TRANSACTIONS")
        self.__messages = {}


message_repository = MessageRepository()
