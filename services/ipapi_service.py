from services import BaseAPI
from common import config


class IPAPIService(BaseAPI):
    __TOKEN__ = "?access_key=" + config.get_ip_api_token()
    __BASE_URL__ = BaseAPI.__HTTP__ + "api.ipapi.com/api"
    __XML_OUT__ = "&output=xml"
    __JSON_OUT__ = "&output=json"
    __WITH_CALLBACK__ = "&callback="
    __WITH_HOSTNAME__ = "&hostname=1"
    __WITH_SECURITY__ = "&security=1"
    __WITH_FIELDS__ = "&fields="
    __WITH_LANGUAGE__ = "&language="

    __allowed_languages__ = ['en', 'de', 'ed', 'fr', 'ja', 'pt-br', 'ru', 'zh']
    __preform_order__ = []
    __on_preform_url__ = ""
    __as__ = None

    __JSON__ = 1
    __XML__ = 2

    def __init__(self):
        super(IPAPIService, self).__init__(self.__BASE_URL__)

    @classmethod
    def check_host(cls, host):
        cls.__preform_order__.append(f'/{host}' + cls.__TOKEN__)
        return cls

    @classmethod
    def with_hostname(cls):
        cls.__preform_order__.append(cls.__WITH_HOSTNAME__)
        return cls

    @classmethod
    def with_security(cls):
        cls.__preform_order__.append(cls.__WITH_SECURITY__)
        return cls

    @classmethod
    def with_language(cls, lang='en'):
        if lang not in cls.__allowed_languages__:
            error_msg = f"Language {lang} is not in supported languages :  {cls.__allowed_languages__.__str__()}"
            raise InterruptedError(error_msg)
        cls.__preform_order__.append(cls.__WITH_LANGUAGE__ + lang)
        return cls

    @classmethod
    def with_fields(cls, *fields):
        order = ""
        for i in range(len(fields)):
            if i != len(fields)-1:
                order += str(fields[i]) + ","
            else:
                order += str(fields[i])
        cls.__preform_order__.append(cls.__WITH_FIELDS__ + order)
        return cls

    @classmethod
    def with_callback(cls, callback=None):
        cls.__preform_order__.append(cls.__WITH_CALLBACK__ + callback)
        return cls

    @classmethod
    def as_response(cls):
        cls.__preform_order__.append(cls.__JSON_OUT__)
        cls.__as__ = 0
        return cls

    @classmethod
    def as_json(cls):
        cls.__preform_order__.append(cls.__JSON_OUT__)
        cls.__as__ = 1
        return cls

    @classmethod
    def as_xml(cls):
        cls.__preform_order__.append(cls.__XML_OUT__)
        cls.__as__ = 2
        return cls

    @classmethod
    def build(cls):
        cls.__on_preform_url__ = cls.__BASE_URL__
        for order in cls.__preform_order__:
            cls.__on_preform_url__ += order
        return cls

    @staticmethod
    def preform():
        if IPAPIService.__as__ is None:
            error_msg = "Must specify output `.as_json()` , `.as_response()` or `.as_xml()` before `.build().preform()`"
            raise InterruptedError(error_msg)
        elif IPAPIService.__as__ == IPAPIService.__JSON__:
            return IPAPIService.get(self=IPAPIService, url=IPAPIService.__on_preform_url__).json()
        elif IPAPIService.__as__ == IPAPIService.__XML__:
            return IPAPIService.get(self=IPAPIService, url=IPAPIService.__on_preform_url__).text
        else:
            return IPAPIService.get(self=IPAPIService, url=IPAPIService.__on_preform_url__)


if __name__ == '__main__':
    ipapi = IPAPIService()
    data = ipapi.check_host("61.101.12.55").with_language().with_fields().as_json().build().preform()
    print(data)
