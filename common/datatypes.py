from sqlalchemy import Column, Text, JSON, Float
from common.database import Base


class Fingerprints(Base):
    __tablename__ = "fingerprints_tbl"
    uid = Column(Text(), unique=True, primary_key=True)
    ip = Column(Text(), unique=False, nullable=False)
    hostname = Column(Text(), unique=False, nullable=False)
    city = Column(Text(), unique=False, nullable=False)
    continent_code = Column(Text(), unique=False, nullable=False)
    continent_name = Column(Text(), unique=False, nullable=False)
    country_code = Column(Text(), unique=False, nullable=False)
    country_name = Column(Text(), unique=False, nullable=False)
    ip_type = Column(Text(), unique=False, nullable=False)
    region_code = Column(Text(), unique=False, nullable=False)
    region_name = Column(Text(), unique=False, nullable=False)
    zipcode = Column(Text(), unique=False, nullable=False)
    latitude = Column(Float(), unique=False, nullable=False)
    longitude = Column(Float(), unique=False, nullable=False)
    location = Column(JSON(), unique=False, nullable=False)
    security = Column(JSON(), unique=False, nullable=False)
    time_created = Column(Text(), unique=True, nullable=False)
    request_path = Column(Text(), unique=False, nullable=True)
    request_params = Column(Text(), unique=False, nullable=True)
    ssl_cert_chain = Column(JSON(), unique=False, nullable=False)
    ssl_configuration = Column(JSON(), unique=False, nullable=False)
    infra_analysis = Column(JSON(), unique=False, nullable=False)
    malware_check = Column(JSON(), unique=False, nullable=False)
    connected_domains = Column(JSON(), unique=False, nullable=False)
    reputation = Column(JSON(), unique=False, nullable=False)

    def __init__(self, uid=None, ip=None, hostname=None, city=None, country_code=None, country_name=None, ip_type=None,
                 continent_code=None, continent_name=None, region_code=None, region_name=None, zipcode=None,
                 latitude=None, longitude=None, location=None, security=None, time_created=None, request_path=None,
                 request_params=None, ssl_cert_chain=None, ssl_configuration=None, infra_analysis=infra_analysis,
                 malware_check=None, connected_domains=None, reputation=None):
        self.uid = uid
        self.ip = ip
        self.hostname = hostname
        self.city = city
        self.country_code = country_code
        self.country_name = country_name
        self.ip_type = ip_type
        self.continent_code = continent_code
        self.continent_name = continent_name
        self.region_code = region_code
        self.region_name = region_name
        self.zipcode = zipcode
        self.latitude = latitude
        self.longitude = longitude
        self.location = location
        self.security = security
        self.time_created = time_created
        self.request_path = request_path
        self.request_params = request_params
        self.ssl_cert_chain = ssl_cert_chain
        self.ssl_configuration = ssl_configuration
        self.infra_analysis = infra_analysis
        self.malware_check = malware_check
        self.connected_domains = connected_domains
        self.reputation = reputation

    def __repr__(self):
        return '<Fingerprint %r>' % self.uid
