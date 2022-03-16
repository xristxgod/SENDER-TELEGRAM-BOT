import unittest

from src.sender import send_to_bot

class TestSender(unittest.IsolatedAsyncioTestCase):

    async def test_send_to_bot(self):
        result = await send_to_bot(text="TEST MESSAGE")
        self.assertEqual(type(result), bool)
        self.assertTrue(result)