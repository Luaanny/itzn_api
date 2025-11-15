from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.reserva import Reserva
from datetime import date
from app.core.exceptions import conflict

def check_if_room_is_available(reservation_date: date, db: Session):
    room_conflict_query = db.scalar(select(Reserva).where(
        Reserva.data_reserva == reservation_date
    ))

    if room_conflict_query:
        return conflict(
            detail='A sala não está disponível nesse dia.'
        )

    return True