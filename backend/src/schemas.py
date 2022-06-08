from typing import Optional, List, Dict

from pydantic import BaseModel, Field

from config import decimals


# <<<====================================>>> Body <<<================================================================>>>


# USER BOT
class BodyRegUser(BaseModel):
    """Adding new users"""
    email: str = Field(description="Email of the registered (new) user")
    phone: str = Field(description="The phone number of the registered (new) user")
    fio: str = Field(description="Surname, first name, family name of the registered (new) user")


# USER BOT
class BodyBalance(BaseModel):
    """Replenishment/debiting of funds from the user"""
    userName: str = Field(description="The username of the user whose balance was replenished/debited")
    phone: str = Field(description="The phone number of the user whose balance was replenished/debited")
    fio: str = Field(description="Surname, first name, family name of the user whose balance was replenished/debited")
    network: str = Field(description="The network where the deposit/debit occurred")
    amount: str = Field(description="The number of coins that have been replenished/debited")

    def __init__(self, **kwargs):
        super(BodyBalance, self).__init__(**kwargs)
        if isinstance(self.amount, str):
            self.amount = "%.8f" % decimals.create_decimal(self.amount)


# USER BOT
class BodyVerificationUser(BaseModel):
    email: str = Field(description="The email address of the verified user")
    phone: str = Field(description="The phone number of the verified user")
    fio: str = Field(description="Last name, first name, patronymic of the verified user")


# P2P BOT
class BodyP2PEvent(BaseModel):
    phone: str
    currencyFrom: str
    currencyTo: str
    amountIn: str
    amountOut: str


# TBO BOT
class BodyTBOMessage(BaseModel):
    email: str = Field(description="Sender's email")
    phone: str = Field(description="Sender's phone number")
    fio: str = Field(description="Sender's full name")
    userId: int = Field(description="ID of the user who wants to send the transaction.")
    nodeTransactionId: int = Field(description="Transaction ID")
    network: str = Field(description="Network")
    outputs: List[Dict] = Field(description="The recipient/s of the transaction and the amount sent!")


class BodyTelegramMessage(BaseModel):
    userId: int = Field(description="ID of the user who wants to send the transaction.")
    nodeTransactionId: int = Field(description="Transaction ID")
    network: str = Field(description="Network")
    status: bool = Field(description="Approved is True | Reject is False")
    outputs: Optional[List[Dict]] = Field(
        description="The recipient/s of the transaction and the amount sent!", default=[{}]
    )


# <<<====================================>>> Response <<<============================================================>>>


class ResponseStatus(BaseModel):
    """The response about the successful sending of the message"""
    status: bool
    messageError: Optional[str]

    def __init__(self, **kwargs):
        super(ResponseStatus, self).__init__(**kwargs)
        if self.messageError is None:
            del self.messageError


class ResponseRepositoryCache(BaseModel):
    message: Dict
