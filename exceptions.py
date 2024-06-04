from fastapi import HTTPException
from typing_extensions import Annotated , Doc
from typing import Any,Dict


class NotFoundException(HTTPException):
    def __init__(self , detail: str = "not found"):
        super().__init__(status_code =404, detail = detail)