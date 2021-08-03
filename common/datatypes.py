import json

from sqlalchemy import Column, Text, JSON, Float, DateTime
from common.database import Base
from datetime import datetime
from uuid import uuid5, NAMESPACE_URL
from lambdas import stamp


class Fingerprints(Base):
    __tablename__ = "fingerprints_tbl"
    uid = Column(Text(), unique=True, primary_key=True)
    ip = Column(Text(), unique=False, nullable=True, default="EMPTY")
    hostname = Column(Text(), unique=False, nullable=True, default="EMPTY")
    city = Column(Text(), unique=False, nullable=True, default="EMPTY")
    continent_code = Column(Text(), unique=False, nullable=True, default="EMPTY")
    continent_name = Column(Text(), unique=False, nullable=True, default="EMPTY")
    country_code = Column(Text(), unique=False, nullable=True, default="EMPTY")
    country_name = Column(Text(), unique=False, nullable=True, default="EMPTY")
    ip_type = Column(Text(), unique=False, nullable=True, default="EMPTY")
    region_code = Column(Text(), unique=False, nullable=True, default="EMPTY")
    region_name = Column(Text(), unique=False, nullable=True, default="EMPTY")
    zipcode = Column(Text(), unique=False, nullable=True, default="EMPTY")
    latitude = Column(Float(), unique=False, nullable=True, default=0.0)
    longitude = Column(Float(), unique=False, nullable=True, default=0.0)
    location = Column(JSON(), unique=False, nullable=True, default=json.dumps({}))
    security = Column(JSON(), unique=False, nullable=True, default=json.dumps({}))
    time_created = Column(Text(), unique=True, nullable=True, default="EMPTY")
    request_path = Column(Text(), unique=False, nullable=True, default="EMPTY")
    request_params = Column(Text(), unique=False, nullable=True, default="EMPTY")
    ssl_cert_chain = Column(JSON(), unique=False, nullable=True, default=json.dumps({}))
    ssl_configuration = Column(JSON(), unique=False, nullable=True, default=json.dumps({}))
    infra_analysis = Column(JSON(), unique=False, nullable=True, default=json.dumps({}))
    malware_check = Column(JSON(), unique=False, nullable=True, default=json.dumps({}))
    connected_domains = Column(JSON(), unique=False, nullable=True, default=json.dumps({}))
    reputation = Column(JSON(), unique=False, nullable=True, default=json.dumps({}))

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


class Targets(Base):
    __tablename__ = "targets_tbl"
    tid = Column(Text(), unique=True, primary_key=True)
    email = Column(Text(), unique=False, nullable=False)
    first_name = Column(Text(), unique=False, nullable=False)
    last_name = Column(Text(), unique=False, nullable=False)
    time_created = Column(DateTime(), unique=False, nullable=False)
    token = Column(Text(), unique=False, nullable=False)

    def __init__(self, email=None, first_name=None, last_name=None, token=None):
        self.tid = uuid5(NAMESPACE_URL, f'{email}-{stamp()}').__str__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.token = token
        self.time_created = datetime.now()

    def __repr__(self):
        return '<Target %r>' % self.tid
