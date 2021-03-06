from fastapi import FastAPI, Request, Response
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime

from enums import StatusType, MediaType
from common.datatypes import Fingerprints
from common.database import db_session
from lambdas import gen_UUID, EncodeAES, DecodeAES, EncodeHeader, DecodeHeader, stamp
from typing import Optional
from services.ipapi_service import IPAPIService
from services.tip_service import TIPService


app = FastAPI()
app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.middleware('http')
async def add_fingerprint_record(request: Request, call_next):
    try:
        response: Response = await call_next(request)

        ipapi_data = await ipapi_recon(request.client.host)

        uid = gen_UUID(request.client.host).__str__()
        ip = ipapi_data['ip'] if 'ip' in ipapi_data else None
        hostname = ipapi_data['hostname'] if 'hostname' in ipapi_data else None
        ip_type = ipapi_data['type'] if 'type' in ipapi_data else None
        continent_code = ipapi_data['continent_code'] if 'continent_code' in ipapi_data else None
        continent_name = ipapi_data['continent_name'] if 'continent_name' in ipapi_data else None
        country_code = ipapi_data['country_code'] if 'country_code' in ipapi_data else None
        country_name = ipapi_data['country_name'] if 'country_name' in ipapi_data else None
        region_code = ipapi_data['region_code'] if 'region_code' in ipapi_data else None
        region_name = ipapi_data['region_name'] if 'region_name' in ipapi_data else None
        city = ipapi_data['city'] if 'city' in ipapi_data else None
        zipcode = ipapi_data['zip'] if 'zip' in ipapi_data else None
        latitude = ipapi_data['latitude'] if 'latitude' in ipapi_data else None
        longitude = ipapi_data['longitude'] if 'longitude' in ipapi_data else None
        location = ipapi_data['location'] if 'location' in ipapi_data else None
        security = ipapi_data['security'] if 'security' in ipapi_data else None

        tip_data = await tip_recon(hostname)
        infra_analysis = tip_data['infrastructureAnalysis']
        ssl_cert_chain = tip_data['sslCertificatesChain']
        ssl_configuration = tip_data['sslConfiguration']
        malware_check = tip_data['malwareCheck']
        connected_domains = tip_data['connectedDomains']
        reputation = tip_data['reputation']

        fingerprint = Fingerprints(uid=uid, ip=ip, hostname=hostname, ip_type=ip_type, continent_code=continent_code,
                                   country_name=continent_name, country_code=country_code, continent_name=country_name,
                                   region_code=region_code, region_name=region_name, city=city, zipcode=zipcode,
                                   latitude=latitude, longitude=longitude, location=location, security=security,
                                   time_created=str(datetime.now()), request_path=request.path_params.__str__(),
                                   request_params=request.query_params.__str__(), infra_analysis=infra_analysis,
                                   ssl_cert_chain=ssl_cert_chain, ssl_configuration=ssl_configuration,
                                   malware_check=malware_check, connected_domains=connected_domains,
                                   reputation=reputation)
        db_session.add(fingerprint)
        db_session.commit()
        json = jsonable_encoder(obj=response)
        return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=200)
    except Exception as e:
        content = {
            "status": StatusType.FAILED.value,
            "host": request.client.host,
            "timestamp": stamp()
        }
        json = jsonable_encoder(obj=content)
        return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=404)


@app.middleware('http')
async def add_recon_headers(request: Request, call_next):
    try:
        response: Response = await call_next(request)
        fingerprint: Optional[Fingerprints] = Fingerprints.query.filter_by(ip=request.client.host).first()
        if not fingerprint:
            content = {
                "status": StatusType.FAILED.value,
                "timestamp": stamp()
            }
            json = jsonable_encoder(obj=content)
            return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=404)
        response.headers["X-RECON-Internet-ID"] = fingerprint.uid
        response.headers["X-RECON-IP"] = EncodeHeader(data=fingerprint.ip).decode()
        response.headers["X-RECON-CITY"] = EncodeHeader(data=fingerprint.city).decode()
        response.headers["X-RECON-REGION-CODE"] = EncodeHeader(data=fingerprint.region_code).decode()
        response.headers["X-RECON-COUNTRY-NAME"] = EncodeHeader(data=fingerprint.country_name).decode()
        response.headers["X-RECON-COUNTRY-CODE"] = EncodeHeader(data=fingerprint.country_code).decode()
        response.headers["X-RECON-CONTINENT-CODE"] = EncodeHeader(data=fingerprint.continent_code).decode()
        response.headers["X-RECON-LATITUDE"] = EncodeHeader(data=fingerprint.latitude).decode()
        response.headers["X-RECON-LONGITUDE"] = EncodeHeader(data=fingerprint.longitude).decode()
        response.headers["X-RECON-LOCATION"] = EncodeHeader(data=fingerprint.location).decode()
        response.headers["X-RECON-SECURITY"] = EncodeHeader(data=fingerprint.security).decode()

        response.headers["X-RECON-THREAT-INTELLIGENCE-DATA"] = EncodeHeader(data=tip_data).decode()
        json = jsonable_encoder(obj=response)
        return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=200)
    except Exception as e:
        content = {
            "status": StatusType.TRACKED.value,
            "host": request.client.host,
            "timestamp": stamp()
        }
        json = jsonable_encoder(obj=content)
        return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=404)


async def ipapi_recon(host, lang='en'):
    try:
        data = IPAPIService().check_host(host).with_hostname().with_security().with_language(lang=lang).as_json() \
            .build().preform()
        return data
    except Exception as e:
        content = {
            "status": StatusType.TRACKED.value,
            "host": host,
            "timestamp": stamp()
        }
        json = jsonable_encoder(obj=content)
        return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=404)


async def tip_recon(domain):
    try:
        data = TIPService().check_domain(domain_name=domain).gather().preform()
        return data
    except Exception as e:
        content = {
            "status": StatusType.TRACKED.value,
            "host": domain,
            "timestamp": stamp()
        }
        json = jsonable_encoder(obj=content)
        return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=404)


@app.get("/")
def index():
    content = {"status": None, "timestamp": None, "message": None}
    try:
        content["status"] = StatusType.SUCCESS.value
        content["timestamp"] = stamp()
        content["message"] = "data collected"
        json = jsonable_encoder(obj=content)
        return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=200)
    except Exception as e:
        content["status"] = StatusType.TRACKED.value
        content["timestamp"] = stamp()
        content["message"] = "nothing happens"
        json = jsonable_encoder(obj=content)
        return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=404)


if __name__ == '__main__':
    import uvicorn, os
    from common import config
    crt = os.path.join(config.get_root_path(), 'resources', 'localhost.crt')
    pem = os.path.join(config.get_root_path(), 'resources', 'localhost.key')
    uvicorn.run(app, host="0.0.0.0", port=8443, ssl_certfile=crt, ssl_keyfile=pem)
