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

    def __init__(self, uid=None, ip=None, hostname=None, city=None, country_code=None, country_name=None, ip_type=None,
                 continent_code=None, continent_name=None, region_code=None, region_name=None, zipcode=None,
                 latitude=None, longitude=None, location=None, security=None):
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

    def __repr__(self):
        return '<Fingerprint %r>' % self.id
