import asyncio
from pprint import pprint
import unittest
from bot.conf import bot_bridge
from genshin import Client
from unittest.async_case import IsolatedAsyncioTestCase

class test_genshin_client(IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        cookies = {
            "ltuid" : bot_bridge.ltuid,
            "ltoken" : bot_bridge.ltoken,
        }
        self.hoyoclient = Client(cookies=cookies)
    async def test_get_battlesuits(self):
        battlesuits = await self.hoyoclient.get_honkai_battlesuits(
            103304315
        )
        print(len(battlesuits))
        pprint(battlesuits[0])
        pprint(battlesuits[1])
        pprint(battlesuits[11])