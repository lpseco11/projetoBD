from enum import Enum


class StatusCodes(Enum):
    OK = 200
    BadRequest = 400
    Unauthorized = 401
    PaymentRequired = 402
    Forbidden = 403
    NotFound = 404
    InternalServerError = 500
    NotImplemented = 501
