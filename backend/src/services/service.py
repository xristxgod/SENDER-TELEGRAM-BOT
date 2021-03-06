from src.schemas import BodyTBOMessage, BodyTelegramMessage
from src.services.parser import MessageParser
from src.services.sender import SenderToSite, Sender
from src.helper.types import SetMessage
from src.helper.repository import message_repository
from config import Config, logger


class TBOService:

    @staticmethod
    async def set_transaction(body: BodyTBOMessage) -> bool:
        supports_info = await MessageParser.send_approved_event(body=body)
        if supports_info is not None:
            await message_repository.set_message(
                data=SetMessage(
                    userId=body.userId,
                    network=body.network,
                    nodeTransactionId=body.nodeTransactionId,
                    outputs=body.outputs
                ),
                supports_info=supports_info
            )
            return True
        return False

    @staticmethod
    async def update_transaction(body: BodyTelegramMessage) -> bool:
        transaction = await message_repository.get_message(user_id=body.userId, network=body.network)
        try:
            if transaction is not None:
                status = await SenderToSite.send_to_site(
                    body=SetMessage(
                        userId=body.userId, network=body.network, nodeTransactionId=body.nodeTransactionId,
                        outputs=transaction[2]
                    ),
                    status=body.status
                )
                if status:
                    await message_repository.delete_message(user_id=body.userId, network=body.network)
                    if body.text:
                        await Sender.edit_message(
                            support_info=transaction[3], text=body.text, tb_token=Config.BOT_APPROVED_TOKEN
                        )
                return status
            return True
        except Exception as error:
            logger.error(f"ERROR: {error}")
            return False
