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

def server_error(detail: str = 'Internal Server Error'):
    raise HTTPException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        detail=detail,
    )