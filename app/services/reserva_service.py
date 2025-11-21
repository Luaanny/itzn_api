from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.reserva import Reserva
from datetime import date
from app.core.exceptions import conflict, unauthorized, not_found
from app.schemas.reserva import CriarReserva, DeletarReserva, AtualizarReserva, AlterarStatus
from app.services import (post, delete, put, get_all_user_resources, get)
from app.services.google_calendar import create_reservation_event

def check_if_room_is_available(reservation_date: date, db: Session):
    room_conflict_query = db.scalar(select(Reserva).where(
        Reserva.data_reserva == reservation_date,
        Reserva.cancelado == False
    ))

    if room_conflict_query:
        return conflict(
            detail='A sala não está disponível nesse dia.'
        )

    return True

def post_reservation(db: Session, create_schema: CriarReserva):
    check_if_room_is_available(reservation_date=create_schema.data_reserva, db=db)

    nova_reserva = post(resource=Reserva, create_schema=create_schema, db=db)

    try:
        google_id = create_reservation_event(create_schema)
        if google_id:
            nova_reserva.google_event_id = google_id
            db.add(nova_reserva)
            db.commit()
            db.refresh(nova_reserva)
    except Exception as e:
        print(f"Falha na integração Google: {e}")

    return nova_reserva

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

def update_status(db: Session,reservation_id: int, update_schema: AlterarStatus):
    db_reservation = get(db=db, resource=Reserva, resource_id=reservation_id, detail='Reserva não encontrada')

    if db_reservation.changed and db_reservation.changed_by != update_schema.email_usuario:
        return conflict(detail='O status dessa reserva já foi modificada por outro usuário.')

    if db_reservation.email_usuario == update_schema.email_usuario:
        return unauthorized('Você não pode mudas o status da própria reserva')

    db_reservation.status = update_schema.status
    db_reservation.alterado_por = update_schema.email_usuario
    db_reservation.alterado_por = True

    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def get_canceled_reservations(db: Session, user_email: str):
    canceled_reservations = db.scalars(select(Reserva).where(
        Reserva.email_usuario == user_email,
        Reserva.cancelado == True
    )).all()

    return {'reservas': canceled_reservations} if canceled_reservations else \
        not_found('Nenhuma reserva cancelada por esse usuário até o momento.')
