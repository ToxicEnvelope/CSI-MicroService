from enum import Enum


class StatusType(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"
    TRACKED = "tracked"


class MediaType(Enum):
    APPLICATION_JSON = "application/json"
    APPLICATION_ZIP = "application/zip"
    APPLICATION_OCTET = "application/octet-stream"
    APPLICATION_XML = "application/xml"
    PLAIN_TEXT = "plain/text"
