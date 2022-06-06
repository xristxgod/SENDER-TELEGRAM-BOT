import fastapi

from src.schemas import BodyRegUser, BodyBalance, BodyVerificationUser, ResponseStatus, BodyP2PEvent, BodyTBOStatus
from src.service import (
    send_if_req_new_user, send_if_dec_or_add_balance,
    send_if_verification_user, send_p2p_event,
    send_message_approved
)

router = fastapi.APIRouter()


@router.post(
    "/reg-user",
    response_model=ResponseStatus,
    description="This method provides the bot with information about the new user"
)
async def reg_user(body: BodyRegUser) -> ResponseStatus:
    return ResponseStatus(status=(await send_if_req_new_user(body=body)))


@router.post(
    "/balance/{method}",
    response_model=ResponseStatus,
    description="This method sends the bot information about replenishment/debiting from the user"
)
async def balance(method: str, body: BodyBalance) -> ResponseStatus:
    if method in ["add", "dec"]:
        return ResponseStatus(status=(await send_if_dec_or_add_balance(body=body, status=method)))
    else:
        raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail='This method was not found.')


@router.put(
    "/user/verification",
    response_model=ResponseStatus,
    description="The method for sending that the user has been verified"
)
async def verification(body: BodyVerificationUser):
    return ResponseStatus(status=(await send_if_verification_user(body=body)))


@router.put(
    "/p2p/order/create",
    response_model=ResponseStatus,
    description="The method for sending that the user creates new order on P2P service"
)
async def p2p_create(body: BodyP2PEvent):
    return ResponseStatus(status=(await send_p2p_event(body=body)))

@router.post(
    "/send/large-money",
    response_model=ResponseStatus,
    description=""
)
async def large_money(body: BodyTBOStatus):
    return ResponseStatus(status=await send_message_approved(body=body))
