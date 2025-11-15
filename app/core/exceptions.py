from fastapi.exceptions import HTTPException
from http import HTTPStatus

def unauthorized(detail: str = 'Unauthorized'):
    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail=detail,
    )

def not_found(detail: str = 'Not Found'):
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail=detail,
    )

def conflict(detail: str = 'Conflict'):
    raise HTTPException(
        status_code=HTTPStatus.CONFLICT,
        detail=detail,
    )