import unittest

from src.schemas import BodyRegUser, BodyBalance
from src.service import send_if_req_new_user, send_if_dec_or_add_balance


class TestService(unittest.IsolatedAsyncioTestCase):

    async def test_send_if_req_new_user(self):
        result = await send_if_req_new_user(BodyRegUser(**{
            "email": "test_email@test.com",
            "phone": "+790000000",
            "fio": "Testov Test Testovich"
        }))
        self.assertEqual(type(result), bool)
        self.assertTrue(result)

    async def test_send_if_dec_or_add_balance(self):
        for stat in ["add", "dec"]:
            result = await send_if_dec_or_add_balance(BodyBalance(**{
                "userName": "test.testov",
                "phone": "+790000000",
                "fio": "Testov Test Testovich",
                "network": "TRON USDT",
                "amount": "1488.8841"
            }), status=stat)
            self.assertEqual(type(result), bool)
            self.assertTrue(result)
