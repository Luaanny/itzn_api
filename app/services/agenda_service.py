from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.agendamento import Agendamento
from app.core.exceptions import conflict, not_found
from app.schemas.agenda import CriarAgenda, DeletarAgenda, AtualizarAgenda
from app.services import post, get_all_user_resources, delete, put
from app.services.reserva_service import check_if_room_is_available
from app.services.google_calendar import create_appointment_event


def check_if_computer_is_available(db: Session, computer_number: int,
                                   reservation_date: date, reservation_hour: int):
    computer_conflict_query = db.scalar(select(Agendamento).where(
        Agendamento.numero_computador == computer_number,
        Agendamento.data_agendamento == reservation_date,
        Agendamento.hora_inicio == reservation_hour,
        Agendamento.cancelado == False
    ))

    if computer_conflict_query:
        return conflict(detail='Esse computador não está disponível no momento.')

    return True


def post_appointment(db: Session, create_schema: CriarAgenda):
    check_if_room_is_available(db=db, reservation_date=create_schema.data_agendamento)
    check_if_computer_is_available(db=db, computer_number=create_schema.numero_computador,
                                   reservation_date=create_schema.data_agendamento,
                                   reservation_hour=create_schema.hora_inicio)

    novo_agendamento = post(db=db, create_schema=create_schema, resource=Agendamento)

    try:
        google_id = create_appointment_event(create_schema)
        if google_id:
            novo_agendamento.google_event_id = google_id
            db.add(novo_agendamento)
            db.commit()
            db.refresh(novo_agendamento)
    except Exception as e:
        print(f"Falha na integração Google: {e}")

    return novo_agendamento


def get_all_user_appointments(db: Session, user_email: str):
    agendamentos = get_all_user_resources(db=db, user_email=user_email, resource=Agendamento,
                                          detail='Nenhum agendamento encontrado para esse usuário.')

    return {"agendamentos": agendamentos}

def delete_user_appointment(db: Session, resource_id: int, delete_schema: DeletarAgenda):
    return delete(delete_schema=delete_schema, db=db, resource=Agendamento, resource_id=resource_id,
                  detail='Nenhum agendamento encontrado.')

def update_user_appointment(db: Session, resource_id: int, update_schema: AtualizarAgenda):
    return put(update_schema=update_schema, db=db, resource=Agendamento, resource_id=resource_id,
               detail='Nenhum agendamento encontrado.')

def get_canceled_appointments(db: Session, user_email: str):
    canceled_reservations = db.scalars(select(Agendamento).where(
        Agendamento.email_usuario == user_email,
        Agendamento.cancelado == True
    )).all()

    return {'agendamentos': canceled_reservations} if canceled_reservations else \
        not_found('Nenhuma reserva cancelada por esse usuário até o momento.')
