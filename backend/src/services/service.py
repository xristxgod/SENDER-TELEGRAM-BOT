from src.schemas import BodyTBOMessage
from src.services.parser import MessageParser
from src.helper.types import SetMessage
from src.helper.repository import message_repository

class TBOService:

    @staticmethod
    async def set_transaction(body: BodyTBOMessage) -> bool:
        message_repository.set_message(data=SetMessage(
            userId=body.userId,
            network=body.network,
            nodeTransactionId=body.nodeTransactionId,
            outputs=body.outputs
        ))
        return await MessageParser.send_approved_event(body=body)

