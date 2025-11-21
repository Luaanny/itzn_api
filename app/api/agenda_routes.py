from fastapi import APIRouter, Depends
from http import HTTPStatus

from pydantic import EmailStr

from app.core.security import get_api_key
from app.core.annotateds import session_type, check_api_key
from app.schemas.agenda import (CriarAgenda, RespostaAgenda, ListaAgenda, 
                                DeletarAgenda, AtualizarAgenda)
from app.services.agenda_service import (post_appointment, get_all_user_appointments,
                                        delete_user_appointment, update_user_appointment, get_canceled_appointments)

router = APIRouter()


@router.post("", status_code=HTTPStatus.CREATED, response_model=RespostaAgenda)
def criar_agendamento(
        agenda: CriarAgenda,
        db: session_type,
        api_key: check_api_key
):
    return post_appointment(db=db, create_schema=agenda)


@router.get("", response_model=ListaAgenda)
def resgatar_agendamentos(
        user_email: EmailStr,
        db: session_type,
        api_key: check_api_key
):
    return get_all_user_appointments(db=db, user_email=user_email)

@router.get("/cancelados", response_model=ListaAgenda)
def resgatar_agendamentos_cancelados(
    db: session_type,
    user_email: EmailStr,
    api_key: check_api_key
):
    return get_canceled_appointments(db=db, user_email=user_email)

@router.delete("/{agenda_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_agendamento(
        agenda_id: int,
        db: session_type,
        delete_data: DeletarAgenda,
        api_key: check_api_key
):
    return delete_user_appointment(delete_schema=delete_data, resource_id=agenda_id, db=db)

@router.put("/{agenda_id}", response_model=RespostaAgenda)
def atualizar_agendamento(
        agenda_id: int,
        db: session_type,
        update_data: AtualizarAgenda,
        api_key: check_api_key
):
    return update_user_appointment(update_schema=update_data, resource_id=agenda_id, db=db)