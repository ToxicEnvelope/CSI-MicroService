from services import BaseAPI
from common import config


class TIPService(BaseAPI):
    __TOKEN__ = "&apiKey=" + config.get_tip_api_token()
    __BASE_URL__ = BaseAPI.__HTTPS__ + "api.threatintelligenceplatform.com/v1"
    __GENERAL_INFO__ = f"{__BASE_URL__}/infrastructureAnalysis?domainName="
    __SSL_CERT_CHAIN__ = f"{__BASE_URL__}/sslCertificatesChain?domainName="
    __SSL_CONFIGURATION__ = f"{__BASE_URL__}/sslConfiguration?domainName="
    __DOMAIN_MALWARE_CHECK__ = f"{__BASE_URL__}/malwareCheck?domainName="
    __CONNECTED_DOMAINS__ = f"{__BASE_URL__}/connectedDomains?domainName="
    __DOMAIN_REPUTATION__ = f"{__BASE_URL__}/reputation?domainName="

    __domain_to_check__ = ""
    __preform_actions__ = []
    __keys__ = ['infrastructureAnalysis', 'sslCertificatesChain', 'sslConfiguration',
                'malwareCheck', 'connectedDomains', 'reputation']
    __gathered_intelligent_to_response__ = {
    }

    def __init__(self):
        super(TIPService, self).__init__(self.__BASE_URL__)

    @classmethod
    def check_domain(cls, domain_name=None):
        cls.__domain_to_check__ = domain_name
        cls.__general_info() \
            .__ssl_certificate_chain() \
            .__ssl_configuration() \
            .__domain_malware_check() \
            .__connected_domains() \
            .__domain_reputation()
        return cls

    @classmethod
    def gather(cls):
        if cls.__domain_to_check__ is None:
            error_msg = "Must specify DOMAIN using `.check_domain()` before using `.gather()`"
            raise InterruptedError(error_msg)
        for pairs in zip(cls.__keys__, cls.__preform_actions__):
            key, scan_url = pairs
            data = cls.get(self=cls, url=scan_url).json()
            cls.__gathered_intelligent_to_response__.setdefault(key, data)
        return cls

    @staticmethod
    def preform():
        if TIPService:
            return TIPService.__gathered_intelligent_to_response__

    @classmethod
    def __general_info(cls):
        scan_url = cls.__GENERAL_INFO__ + cls.__domain_to_check__ + cls.__TOKEN__
        cls.__preform_actions__.append(scan_url)
        return cls

    @classmethod
    def __ssl_certificate_chain(cls):
        scan_url = cls.__SSL_CERT_CHAIN__ + cls.__domain_to_check__ + cls.__TOKEN__
        cls.__preform_actions__.append(scan_url)
        return cls

    @classmethod
    def __ssl_configuration(cls):
        scan_url = cls.__SSL_CONFIGURATION__ + cls.__domain_to_check__ + cls.__TOKEN__
        cls.__preform_actions__.append(scan_url)
        return cls

    @classmethod
    def __domain_malware_check(cls):
        scan_url = cls.__DOMAIN_MALWARE_CHECK__ + cls.__domain_to_check__ + cls.__TOKEN__
        cls.__preform_actions__.append(scan_url)
        return cls

    @classmethod
    def __connected_domains(cls):
        scan_url = cls.__CONNECTED_DOMAINS__ + cls.__domain_to_check__ + cls.__TOKEN__
        cls.__preform_actions__.append(scan_url)
        return cls

    @classmethod
    def __domain_reputation(cls):
        scan_url = cls.__DOMAIN_REPUTATION__ + cls.__domain_to_check__ + cls.__TOKEN__
        cls.__preform_actions__.append(scan_url)
        return cls


if __name__ == '__main__':
    tip = TIPService()
    print(tip.check_domain("teslathreat.net").gather().preform())
