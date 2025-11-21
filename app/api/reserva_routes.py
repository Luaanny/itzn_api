from http import HTTPStatus

from fastapi import APIRouter
from pydantic import EmailStr

from app.services.reserva_service import (post_reservation, get_user_reservations, delete_reservation,
                                         update_reservation, update_status, get_canceled_reservations)
from app.core.annotateds import session_type
from app.schemas.reserva import (CriarReserva, RespostaReserva, ListaReserva, 
                                 DeletarReserva, AtualizarReserva, AlterarStatus)
from app.core.annotateds import check_api_key

router = APIRouter()

@router.post("", response_model=RespostaReserva, status_code=HTTPStatus.CREATED)
def criar_reserva(
        db: session_type,
        reservation_data: CriarReserva,
        api_key: check_api_key
):
    return post_reservation(db=db, create_schema=reservation_data)

@router.get("", response_model=ListaReserva)
def listar_reservas_do_usuario(
        db: session_type,
        user_email: EmailStr,
        api_key: check_api_key
):
    return get_user_reservations(db=db, user_email=user_email)

@router.get('/canceladas', response_model=ListaReserva)
def listar_reservas_canceladas_do_usuario(
    db: session_type,
    user_email: EmailStr,
    api_key: check_api_key
):
    return get_canceled_reservations(db=db, user_email=user_email)


@router.delete("/{reserva_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_reserva(
        db: session_type,
        reserva_id: int,
        delete_data: DeletarReserva,
        api_key: check_api_key
):
    return delete_reservation(db=db, delete_schema=delete_data, reservation_id=reserva_id)

@router.put("/{reserva_id}", response_model=RespostaReserva)
def atualizar_reserva(
        db: session_type,
        reserva_id: int,
        update_data: AtualizarReserva,
        api_key: check_api_key
):
    return update_reservation(db=db, resource_id=reserva_id, update_schema=update_data)

@router.patch('/{reserva_id}/status', response_model=RespostaReserva)
def mudar_status(
    db: session_type,
    reserva_id: int,
    patch_data: AlterarStatus,
    api_key: check_api_key
):
    return update_status(db=db, reservation_id=reserva_id, update_schema=patch_data)