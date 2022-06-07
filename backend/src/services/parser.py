from src.schemas import BodyRegUser, BodyBalance, BodyVerificationUser, BodyP2PEvent, BodyTBOMessage
from src.services.sender import Sender

from src.helper.utils import Utils
from src.helper.types import SYMBOL
from config import Config


class MessageParser:

    @staticmethod
    async def send_if_req_new_user(body: BodyRegUser) -> bool:
        """Send a message about adding a new user."""
        return await Sender.send_to_bot(tb_token=Config.USER_BOT_TOKEN, admin_ids=Config.USER_BOT_ADMIN_IDS, text=(
            f"{SYMBOL.get('reg')} <b>Новый пользователь</b>\n"
            f"- <b>ФИО</b>: {body.fio}\n"
            f"- <b>Email</b>: {body.email}\n"
            f"- <b>Телефонный номер</b>: {body.phone}"
        ))

    @staticmethod
    async def send_if_dec_or_add_balance(body: BodyBalance, status: str) -> bool:
        """Send a message about replenishing/debiting funds from the user."""
        message = f"{SYMBOL.get('add')} <b>Произошло пополнение: {body.amount} {body.network} </b>" \
            if status == "add" else \
            f"{SYMBOL.get('dec')} <b>Произошло списание: {body.amount} {body.network}</b>"
        return await Sender.send_to_bot(tb_token=Config.USER_BOT_TOKEN, admin_ids=Config.USER_BOT_ADMIN_IDS, text=(
            f"{message}\n"
            f"<b>Имя пользователя</b>: {body.userName}\n"
            f"<b>ФИО</b>: {body.fio}\n"
            f"<b>Телефонный номер</b>: {body.phone}"
        ))

    @staticmethod
    async def send_if_verification_user(body: BodyVerificationUser) -> bool:
        return await Sender.send_to_bot(tb_token=Config.USER_BOT_TOKEN, admin_ids=Config.USER_BOT_ADMIN_IDS, text=(
            f"{SYMBOL.get('ver')} <b>Пользователь прошел верификацию</b>\n"
            f"- <b>ФИО</b>: {body.fio}\n"
            f"- <b>Email</b>: {body.email}\n"
            f"- <b>Телефонный номер</b>: {body.phone}"
        ))

    @staticmethod
    async def send_p2p_event(body: BodyP2PEvent) -> bool:
        return await Sender.send_to_bot(tb_token=Config.P2P_TOKEN, admin_ids=Config.P2P_ADMIN_IDS, text=(
            f"{SYMBOL.get('reg')} <b>Создание заявки</b> на обмен\n"
            f"- <b>Телефонный номер</b>: {body.phone}\n"
            f"- {body.amountIn} {body.currencyFrom} на {body.amountOut} {body.currencyTo}\n"
        ))

    @staticmethod
    async def send_approved_event(body: BodyTBOMessage) -> bool:
        outputs_correct = Utils.get_outputs(outputs=body.outputs, network=body.network)
        data_for_button = Utils.get_hex_data(data={
            "userId": body.userId, "nodeTransactionId": body.nodeTransactionId, "network": body.network
        })
        return await Sender.send_to_support(
            tb_token=Config.BOT_APPROVED_TOKEN,
            support_id=[Config.SUPPORT_ID],
            text=(
                f"{SYMBOL.get('transaction')} <b>Создание заявки на транзакцию</b>\n"
                f"- <b>Телефонный номер:</b> {body.phone}\n"
                f"- <b>Email:</b> {body.email}\n"
                f"- <b>ФИО:</b> {body.fio}\n"
                f"- <b>ID Пользователя:</b> {body.userId} | <b>ID Транзакции:</b> {body.nodeTransactionId}\n"
                f"<<<=====================================================================================>>>\n"
                f"{outputs_correct}"
            ),
            buttons=[
                {"text": f"{SYMBOL.get('approve')} Approve", "callback_data": f"data_approve_{data_for_button}"},
                {"text": f"{SYMBOL.get('reject')} Reject", "callback_data": f"data_reject_{data_for_button}"}
            ]
        )
