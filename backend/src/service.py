from src.schemas import BodyRegUser, BodyBalance, BodyVerificationUser, BodyP2PEvent
from src.sender import send_to_bot
from config import (
    symbol, tb_token, admin_ids, p2p_admin_ids, p2p_tb_token,
    tb_approval_bearer, tb_approval_ids, tb_approval_token, url_approved
)


async def send_if_req_new_user(body: BodyRegUser) -> bool:
    """Send a message about adding a new user."""
    return await send_to_bot(tb_token=tb_token, admin_ids=admin_ids, text=(
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
    return await send_to_bot(tb_token=tb_token, admin_ids=admin_ids, text=(
        f"{message}\n"
        f"<b>Имя пользователя</b>: {body.userName}\n"
        f"<b>ФИО</b>: {body.fio}\n"
        f"<b>Телефонный номер</b>: {body.phone}"
    ))


async def send_if_verification_user(body: BodyVerificationUser) -> bool:
    return await send_to_bot(tb_token=tb_token, admin_ids=admin_ids, text=(
        f"{symbol['ver']} <b>Пользователь прошел верификацию</b>\n"
        f"- <b>ФИО</b>: {body.fio}\n"
        f"- <b>Email</b>: {body.email}\n"
        f"- <b>Телефонный номер</b>: {body.phone}"
    ))


async def send_p2p_event(body: BodyP2PEvent) -> bool:
    return await send_to_bot(tb_token=p2p_tb_token, admin_ids=p2p_admin_ids, text=(
        f"{symbol['reg']} <b>Создание заявки</b> на обмен\n"
        f"- <b>Телефонный номер</b>: {body.phone}\n"
        f"- {body.amountIn} {body.currencyFrom} на {body.amountOut} {body.currencyTo}\n"
    ))


async def send_message_approved(body: BodyTBOStatus) -> bool:
    data = dict(
        userId=body.senderData.userId,
        nodeTransactionId=body.senderData.nodeTransactionId,
        network=body.senderData.network,
        outputs=body.senderData.outputs
    )
    auth = tb_approval_bearer
    status = await send_to_url_put(url=url_approved + "/api/admin/approved", auth=auth, **data)
    if status:
        title = f"{symbol['approved']} <b>Заявка одобрена</b>"
    else:
        title = f"{symbol['rejected']} <b>Заявка отклонена</b>"
        await send_to_url_put(url=url_approved + "/api/admin/reject", auth=auth, **data)

    outputs = ""
    for output in body.senderData.outputs:
        address, amount = list(output.items())[0]
        outputs += f"- <b>От:</b> {address} <b>на сумму:</b> {amount} {body.senderData.network}\n"

    return await send_to_bot(tb_token=tb_approval_token, admin_ids=tb_approval_ids, text=(
        f"{title}\n"
        f"- <b>ФИО</b>: {body.userInfo.fio}\n"
        f"- <b>Email</b>: {body.userInfo.email}\n"
        f"- <b>Телефонный номер</b>: {body.userInfo.phone}\n"
        f"{symbol['transaction']} <b>Транзакция № {body.senderData.nodeTransactionId}</b>\n"
        "<<<=================================================================================>>>\n"
        f"{outputs[:-1]}"
    ))
