import unittest
import typing

import requests

from config import api_url


def _get_response(method, url, data) -> typing.Dict:
    return requests.request(method, url, json=data).json()


class TestApiBot(unittest.TestCase):

    API_URL = api_url
    REG_USER = api_url + "/reg-user"
    ADD_BALANCE = api_url + "/balance/add"
    DEC_BALANCE = api_url + "/balance/dec"

    def test_reg_user(self):
        result = _get_response("POST", TestApiBot.REG_USER, {
            "email": "test_email@test.com",
            "phone": "+790000000",
            "fio": "Testov Test Testovich"
        })
        self.assertEqual(type(result), dict)
        self.assertIn("status", result)
        self.assertTrue(result["status"])

    def test_add_balance(self):
        result = _get_response("POST", TestApiBot.ADD_BALANCE, {
            "userName": "test.testov",
            "phone": "+790000000",
            "fio": "Testov Test Testovich",
            "network": "TRON USDT",
            "amount": "1488.8841"
        })
        self.assertEqual(type(result), dict)
        self.assertIn("status", result)
        self.assertTrue(result["status"])

    def test_dec_balance(self):
        result = _get_response("POST", TestApiBot.DEC_BALANCE, {
            "userName": "test.testov",
            "phone": "+790000000",
            "fio": "Testov Test Testovich",
            "network": "TRON USDT",
            "amount": "8841.1488"
        })
        self.assertEqual(type(result), dict)
        self.assertIn("status", result)
        self.assertTrue(result["status"])
