from src.schemas import BodyTBOMessage, BodyTelegramMessage
from src.services.parser import MessageParser
from src.services.sender import SenderToSite
from src.helper.types import SetMessage
from src.helper.repository import message_repository
from config import logger


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

    @staticmethod
    async def update_transaction(body: BodyTelegramMessage) -> bool:
        transaction = message_repository.get_message(user_id=body.userId, network=body.network)
        try:
            if transaction is not None:
                status = await SenderToSite.send_to_site(body=SetMessage(
                    userId=body.userId, network=body.network, nodeTransactionId=body.nodeTransactionId,
                    outputs=transaction[2]
                ))
                if status:
                    message_repository.delete_message(user_id=body.userId, network=body.network)
                return status
            else:
                status = await SenderToSite.send_to_site(body=SetMessage(
                    userId=body.userId, network=body.network, nodeTransactionId=body.nodeTransactionId,
                    outputs=body.outputs
                ))
                return status
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return True
