import os
from pprint import pprint
import sys
from time import sleep
import unittest
import json
from alib.tracker import ArmandaTracker, UID_Item, HonkaiMember
import logging

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


class t_armtra_basic(unittest.TestCase):
    def setUp(self) -> None:
        source = {
            1244 : {
                "discord_id" : 55555,
                "lv" : 1
            },
            1245 : {
                "discord_id" : 55556,
                "lv" : 2
            }
        }

        self.tracker : ArmandaTracker = ArmandaTracker(
            source = source,
            typ= HonkaiMember
        )

    def test_armtra_init(self) -> None:
        self.assertEqual(self.tracker.__real_data__, {
            "1244" : {
                "discord_id" : 55555,
                "lv" : 1
            },
            "1245" : {
                "discord_id" : 55556,
                "lv" : 2
            }
        })

    def test_armtra_op(self):
        self.tracker.add_member(
            uid=1246,
            discord_id = 55557,
            lv = 3
        )

        self.assertTrue(self.tracker.has_member(uid=1246))
        self.assertIsInstance(self.tracker.get_member(uid=1246), HonkaiMember)

class t_armtra_file(unittest.TestCase):
    def test_1(self):

        source = "test.json"
        if os.path.exists(source):
            os.remove(source)

        self.tracker : ArmandaTracker = ArmandaTracker(
            source = source,
            typ= HonkaiMember,
        )

        self.tracker.add_member(
            uid=1246,
            discord_id = 55557,
            lv = 3
        )
        self.tracker.add_member(
            uid=12999,
            discord_id = 212457,
            lv = 3
        )
        pprint(self.tracker.__real_data__)

        self.tracker.save()
        self.tracker.remove_member(uid=1246)

        sleep(5)
        self.tracker.save()