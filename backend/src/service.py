from src.schemas import BodyRegUser, BodyBalance
from src.sender import send_to_bot
from config import symbol

async def send_if_req_new_user(body: BodyRegUser) -> bool:
    """Send a message about adding a new user."""
    return await send_to_bot(text=(
        f"{symbol['reg']} <b>Новый пользователь</b>\n"
        f"- <b>ФИО</b>: {body.fio}\n"
        f"- <b>Email</b>: {body.email}\n"
        f"- <b>Телефонный номер</b>: {body.phone}"
    ))


async def send_if_dec_or_add_balance(body: BodyBalance, status: str) -> bool:
    """Send a message about replenishing/debiting funds from the user."""
    message = f"{symbol['add']} <b>Произошло пополнение: {body.amount} {body.network} </b>" \
        if status == "add" else \
        f"{symbol['dec']} <b>Произошло списание: {body.amount} {body.network}</b>"
    return await send_to_bot(text=(
        f"{message}\n"
        f"<b>Имя пользователя</b>: {body.userName}\n"
        f"<b>ФИО</b>: {body.fio}\n"
        f"<b>Телефонный номер</b>: {body.phone}"
    ))