from enum import Enum


class StatusType(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"


class MediaType(Enum):
    APPLICATION_JSON = "application/json"
    APPLICATION_XML = "application/xml"
    PLAIN_TEXT = "plain/text"
