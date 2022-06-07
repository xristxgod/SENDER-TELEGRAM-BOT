from typing import List, Dict
from dataclasses import dataclass

import emoji


SYMBOL = {
    "add": emoji.emojize(":green_circle:"),
    "dec": emoji.emojize(":red_circle:"),
    "reg": emoji.emojize(":yellow_circle:"),
    "ver": emoji.emojize(":ok_hand:", language='alias'),
    "user": emoji.emojize(":bust_in_silhouette:"),
    "transaction": emoji.emojize(":money_with_wings:"),
    "approve": emoji.emojize(":check_mark_button:"),
    "reject": emoji.emojize(":cross_mark_button:")
}


# <<<====================================>>> DataClasses <<<=========================================================>>>


@dataclass
class SetMessage:
    userId: int
    network: str
    nodeTransactionId: int
    outputs: List[Dict[str, str]]

    @property
    def to_json(self) -> Dict:
        return self.__dict__


# <<<====================================>>> Repository Utils <<<====================================================>>>


class MessageController:
    """
    This class is used for interaction
    """
    def set_message(self, data: SetMessage) -> bool:
        raise NotImplementedError

    def get_message(self, user_id: int, network: str) -> Dict:
        raise NotImplementedError

    def delete_message(self, user_id: int, network: str) -> bool:
        raise NotImplementedError
