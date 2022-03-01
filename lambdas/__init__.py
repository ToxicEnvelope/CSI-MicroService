import datetime
from uuid import uuid5, NAMESPACE_URL
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
# from common import config
# from pyqrcode import QRCode
# import pyqrcode
# import png


__key__ = get_random_bytes(16)
__cipher__ = AES.new(__key__, AES.MODE_ECB)

# create_qr_url_svg = lambda h, u: u.svg(f'{config.get_qr_repository()}/{h}.svg', scale=8)
# get_qr_image = lambda name: open(f'{config.get_qr_repository()}/{name}.svg', 'r').read()
DateNow = lambda: datetime.datetime.now().isoformat()
GenUUID = lambda host: uuid5(NAMESPACE_URL, DateNow()).hex
EncodeAES = lambda s: b64encode(__cipher__.encrypt(pad(s if isinstance(s, bytes) else s.encode(), AES.block_size)))
DecodeAES = lambda e: unpad(__cipher__.decrypt(b64decode(e)), AES.block_size)

if __name__ == '__main__':
    es = EncodeAES("Hello Wrold!")
    print(es)
    ds = DecodeAES(es)
    print(ds)
