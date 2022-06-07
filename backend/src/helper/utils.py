import json
from typing import List, Dict

from src.helper.types import SYMBOL


class Utils:

    @staticmethod
    def get_outputs(outputs: List[Dict], network: str) -> str:
        outputs_text = ""
        for output in outputs:
            address, amount = list(output.items())[0]
            outputs_text = f"{SYMBOL.get('user')}<b>{address}</b> на сумму: <b>{amount} {network}</b>\n"
        return outputs_text[:-1]

    @staticmethod
    def get_hex_data(data: Dict) -> str:
        return json.dumps(data).encode("utf-8").hex()
