import fastapi

from src.schemas import BodyRegUser, BodyBalance, ResponseStatus
from src.service import send_if_req_new_user, send_if_dec_or_add_balance

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

