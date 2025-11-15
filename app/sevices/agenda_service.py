from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.agendamento import Agendamento
from app.core.exceptions import conflict

def check_if_computer_is_available(db: Session, computer_number: int,
                                   reservation_date: date, reservation_hour: int):
    computer_conflict_query = db.scalar(select(Agendamento).where(
        Agendamento.numero_computador == computer_number,
        Agendamento.data_agendamento == reservation_date,
        Agendamento.hora_inicio == reservation_hour
    ))

    if computer_conflict_query:
        return conflict(detail='Esse computador não está disponível no momento.')

    return True

