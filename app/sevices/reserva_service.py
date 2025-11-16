from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.reserva import Reserva
from datetime import date
from app.core.exceptions import conflict
from app.schemas.reserva import CriarReserva, DeletarReserva, AtualizarReserva
from app.sevices import (post, delete, put, get_all_user_resources)

def check_if_room_is_available(reservation_date: date, db: Session):
    room_conflict_query = db.scalar(select(Reserva).where(
        Reserva.data_reserva == reservation_date
    ))

    if room_conflict_query:
        return conflict(
            detail='A sala não está disponível nesse dia.'
        )

    return True

def post_reservation(db: Session, create_schema: CriarReserva):
    check_if_room_is_available(reservation_date=create_schema.data_reserva, db=db)
    return post(resource=Reserva, create_schema=create_schema, db=db)

def get_user_reservations(db: Session, user_email: str):
    reservas = get_all_user_resources(db=db, user_email=user_email,
                                  resource=Reserva, detail='Nenhum agendamento encontrado para esse usuário.')

    return {"reservas": reservas}

def delete_reservation(db: Session, delete_schema: DeletarReserva, reservation_id: int):
    return delete(resource=Reserva, db=db, delete_schema=delete_schema,
                  detail='Reserva não encontrada.', resource_id=reservation_id)

def update_reservation(db: Session, update_schema: AtualizarReserva, resource_id: int):
    check_if_room_is_available(reservation_date=update_schema.data_reserva, db=db)
    return put(resource=Reserva, update_schema=update_schema, db=db, resource_id=resource_id,
               detail='Reserva não encontrada.')