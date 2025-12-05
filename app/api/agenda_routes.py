from fastapi import APIRouter, Depends, Header
from http import HTTPStatus

from pydantic import EmailStr

from app.core.annotateds import session_type, check_api_key
from app.schemas.agenda import (CriarAgenda, RespostaAgenda, ListaAgenda, 
                                DeletarAgenda, AtualizarAgenda)
from app.schemas.filter import AgendamentoFiltro
from app.services.agenda_service import (post_appointment, get_all_user_appointments, get_all_canceled_appointments,
                                        delete_user_appointment, update_user_appointment, get_canceled_appointments,
                                        get_all_appointments)

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
    db: session_type,
    api_key: check_api_key,
    user_email: EmailStr | None = Header(None, alias="X-User-Email"),
    filter: AgendamentoFiltro = Depends()
):
    if user_email:
        return get_all_user_appointments(db=db, user_email=user_email, filter=filter)
    
    return get_all_appointments(db=db, filter=filter)

@router.get("/cancelados", response_model=ListaAgenda)
def resgatar_agendamentos_cancelados(
    db: session_type,
    api_key: check_api_key,
    user_email: EmailStr | None = Header(None, alias="X-User-Email")
):
    if user_email:
        return get_canceled_appointments(db=db, user_email=user_email)
    return get_all_canceled_appointments(db=db)

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