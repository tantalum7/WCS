
# Library imports
import unittest
import os
import time

# Project imports
from WCS import CryptStore


class WcsTest(unittest.TestCase):

    TEST_FILE_PATH = "testfile1.bin"
    KEY_A = "keyA"
    VALUE_A = "valueA"
    TEST_DICT_GOOD = {"k1": "vstring",
                      10: 20,
                      15.5: 16.6,
                      "kdict": {"vdict": "vdictv"},
                      "klist": ["ornages"]}

    def setUp(self):
        self.wcs = CryptStore.new(self.TEST_FILE_PATH)

    def tearDown(self):
        del self.wcs
        os.remove(self.TEST_FILE_PATH)

    def test_new(self):
        self.assertTrue(os.path.isfile("testfile1.bin"))
        self.assertAlmostEqual(self.wcs.creation_time, time.time(), places=1)

    def test_rebind(self):
        self.wcs[self.KEY_A] = self.VALUE_A
        self._rebind()
        self.assertEqual(self.wcs[self.KEY_A], self.VALUE_A)

    def test_good_keys(self):
        for key, value in self.TEST_DICT_GOOD.items():
            self.wcs[key] = value

        self._rebind()

        for key, value in self.TEST_DICT_GOOD.items():
            self.assertEqual(self.wcs[key], value)

    def test_bad_keys(self):
        with self.assertRaises(TypeError):
            self.wcs[{"bad": "key"}] = "junk"

        for key in self.wcs._RESERVED_KEYS:
            with self.assertRaises(KeyError):
                self.wcs[key] = "some value"

    def test_bad_values(self):
        class unhashableClass:
            pass

        with self.assertRaises(AttributeError):
            self.wcs["bad_value"] = unhashableClass()

    def _rebind(self):
        del self.wcs
        self.wcs = CryptStore(self.TEST_FILE_PATH)

if __name__ == '__main__':
    unittest.main()