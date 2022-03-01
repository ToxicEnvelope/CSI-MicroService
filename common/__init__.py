from os.path import join, dirname, abspath
from json import load

__ROOT_DIR__ = dirname(dirname(abspath(__file__)))


class Singleton(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]


class Config(object, metaclass=Singleton):
    @staticmethod
    def get_qr_repository(): return join(__ROOT_DIR__, 'qr_repository')
    @staticmethod
    def get_host(): return '0.0.0.0'
    @staticmethod
    def get_port(): return 41514
    @staticmethod
    def get_root_path(): return __ROOT_DIR__
    @staticmethod
    def get_server_crt(): return join(__ROOT_DIR__, 'resources', '.crt')
    @staticmethod
    def get_server_key(): return join(__ROOT_DIR__, 'resources', '.key')

    @staticmethod
    def get_ip_api_token():
        with open(join(__ROOT_DIR__, 'resources', 'config.json')) as cfg:
            data = load(cfg)
            return data['Tokens']['IP_API']

    @staticmethod
    def get_tip_api_token():
        with open(join(__ROOT_DIR__, 'resources', 'config.json')) as cfg:
            data = load(cfg)
            return data['Tokens']['TIP_API']

    @staticmethod
    def get_payloads(payload_name):
        return join(__ROOT_DIR__, "payloads", payload_name)
