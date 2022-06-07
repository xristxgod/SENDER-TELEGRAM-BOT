import fastapi

from src.schemas import (
    BodyRegUser, BodyBalance, BodyVerificationUser, BodyTelegramMessage,
    BodyP2PEvent, BodyTBOMessage, ResponseStatus
)
from src.services.parser import MessageParser
from src.services.service import TBOService

router = fastapi.APIRouter()


# <<<====================================>>> User bot <<<============================================================>>>


@router.post(
    "/reg-user",
    response_model=ResponseStatus,
    description="This method provides the bot with information about the new user",
    tags=["USER BOT"]
)
async def reg_user(body: BodyRegUser) -> ResponseStatus:
    return ResponseStatus(status=(await MessageParser.send_if_req_new_user(body=body)))


@router.post(
    "/balance/{method}",
    response_model=ResponseStatus,
    description="This method sends the bot information about replenishment/debiting from the user",
    tags=["USER BOT"]
)
async def balance(method: str, body: BodyBalance) -> ResponseStatus:
    if method in ["add", "dec"]:
        return ResponseStatus(status=(await MessageParser.send_if_dec_or_add_balance(body=body, status=method)))
    else:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail='This method was not found.')


@router.put(
    "/user/verification",
    response_model=ResponseStatus,
    description="The method for sending that the user has been verified",
    tags=["USER BOT"]
)
async def verification(body: BodyVerificationUser):
    return ResponseStatus(status=(await MessageParser.send_if_verification_user(body=body)))


# <<<====================================>>> P2P bot <<<=============================================================>>>


@router.put(
    "/p2p/order/create",
    response_model=ResponseStatus,
    description="The method for sending that the user creates new order on P2P service",
    tags=["P2P BOT"]
)
async def p2p_create(body: BodyP2PEvent):
    return ResponseStatus(status=(await MessageParser.send_p2p_event(body=body)))


# <<<====================================>>> TBO bot <<<=============================================================>>>


@router.put(
    "/send/large-money",
    description="Sending to the bot to confirm the transaction!",
    response_model=ResponseStatus,
    tags=["APPROVED BOT"]
)
async def send_large_money(body: BodyTBOMessage):
    return ResponseStatus(status=(await TBOService.set_transaction(body=body)))


@router.put(
    "/bot/update",
    description="",
    response_model=ResponseStatus,
    tags=["APPROVED BOT HELPER"]
)
async def update_bot(body: BodyTelegramMessage):
    return ResponseStatus(status=(await TBOService.update_transaction(body=body)))


@router.get(
    "/repository/cache",
    description="",
    # response_model="",
    tags=["APPROVED BOT HELPER"]
)
async def get_repository_cache():
    pass