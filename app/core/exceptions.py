from fastapi.exceptions import HTTPException
from http import HTTPStatus

def unauthorized(detail: str = 'Unauthorized'):
    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail=detail,
    )