import pytest
from tests import UnitTest
from lambdas import DateNow, __key__, __cipher__, AES, EncodeAES, DecodeAES


class TestModuleLambdas(UnitTest):
    def test_key_variable(self):
        self.assertEqual(len(__key__), 16, "assert key is not 16 bytes")

    def test_cipher_object(self):
        self.assertEqual(type(__cipher__), type(AES.new(__key__, AES.MODE_ECB)), "assert cipher is not AES object")

    def test_EncodeDecode_Headers(self):
        header = {"Authorization": "Bearer 1234567890-"}.__str__()
        encHeader = EncodeAES(header)
        self.assertNotEqual(encHeader, header, "assert EncodeHeader failed")
        decHeader = DecodeAES(encHeader).decode()
        self.assertEqual(decHeader, header, "assert DecodeHeader failed")

    def test_stamp_function(self):
        from time import time
        self.assertAlmostEqual(DateNow(), int(time().__str__()[:10]), "assert stamp function failed")


if __name__ == '__main__':
    pytest.main()
