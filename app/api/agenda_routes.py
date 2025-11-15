from fastapi import APIRouter
from http import HTTPStatus
from app.schemas.agenda import CriarAgenda, PublicAgenda


router = APIRouter()

@router.post("", status_code=HTTPStatus.CREATED, response_model=PublicAgenda)
def criar_agenda(agenda: CriarAgenda):
    return
    