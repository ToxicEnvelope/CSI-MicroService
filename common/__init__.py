from os.path import join, dirname, abspath
from json import load

__ROOT_DIR__ = dirname(dirname(abspath(__file__)))


class Singleton:
    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)


@Singleton
class Config(object):

    @staticmethod
    def get_qr_repository(): return join(__ROOT_DIR__, 'qr_repository')
    @staticmethod
    def get_host(): return '0.0.0.0'
    @staticmethod
    def get_port(): return 41514

    @staticmethod
    def get_root_path():
        return f"{__ROOT_DIR__}"

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

global config
config = Config.Instance()

if __name__ == '__main__':
    print(config.get_connection_string())
    print(config.get_ip_api_token())
