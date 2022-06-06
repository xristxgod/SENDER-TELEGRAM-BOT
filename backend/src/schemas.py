from pydantic import BaseModel, Field
from config import decimals


class BodyRegUser(BaseModel):
    """Adding new users"""
    email: str = Field(description="Email of the registered (new) user")
    phone: str = Field(description="The phone number of the registered (new) user")
    fio: str = Field(description="Surname, first name, family name of the registered (new) user")


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


class BodyVerificationUser(BaseModel):
    email: str = Field(description="The email address of the verified user")
    phone: str = Field(description="The phone number of the verified user")
    fio: str = Field(description="Last name, first name, patronymic of the verified user")


class ResponseStatus(BaseModel):
    """The response about the successful sending of the message"""
    status: bool


class BodyP2PEvent(BaseModel):
    phone: str
    currencyFrom: str
    currencyTo: str
    amountIn: str
    amountOut: str
