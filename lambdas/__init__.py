from time import time
from uuid import uuid5, NAMESPACE_URL
from common import config
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
# from pyqrcode import QRCode
# import pyqrcode
# import png


__key__ = get_random_bytes(16)
__cipher__ = AES.new(__key__, AES.MODE_CBC)

# create_qr_url_svg = lambda h, u: u.svg(f'{config.get_qr_repository()}/{h}.svg', scale=8)
stamp = lambda: int(time().__str__()[:10])
gen_UUID = lambda host: uuid5(NAMESPACE_URL, f'{stamp()}')
# get_qr_image = lambda name: open(f'{config.get_qr_repository()}/{name}.svg', 'r').read()

EncodeAES = lambda s: b64encode(__cipher__.encrypt(s.encode().zfill(16 - len(s))))
DecodeAES = lambda e: __cipher__.decrypt(b64decode(e))

EncodeHeader = lambda data: b64encode(data.__str__().encode())
DecodeHeader = lambda data: b64decode(data)