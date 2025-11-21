from sqlalchemy.orm import Session
from app.core.exceptions import not_found, unauthorized
from sqlalchemy import select
from app.models.reserva import Reserva
from app.models.agendamento import Agendamento
from app.services.google_calendar import delete_calendar_event


def get_resources(resource: Reserva | Agendamento, db: Session, detail: str = 'Not found'):
    db_resource = db.scalars(select(resource)).all()
    return db_resource if db_resource else not_found(detail)


def get(resource: Reserva | Agendamento, db: Session, resource_id: int, detail: str = 'Not found'):
    db_resource = db.scalar(select(resource).where(resource.id == resource_id))

    return db_resource if db_resource else not_found(detail)


def get_all_user_resources(resource: Reserva | Agendamento, db: Session,
                           user_email: str, detail: str):
    db_resources = db.scalars(select(resource).where(
        resource.email_usuario == user_email,
        resource.cancelado == False
        )).all()

    return db_resources if db_resources else not_found(detail)


def post(resource: Reserva | Agendamento, create_schema, db: Session):
    resource_dict = create_schema.model_dump()
    db_resource = resource(**resource_dict)

    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)

    return db_resource


def put(update_schema, resource_id:int, resource: Reserva | Agendamento, db: Session, detail):
    db_resource = get(resource=resource, resource_id=resource_id, db=db)

    if db_resource.email_usuario != update_schema.email_usuario\
        and not update_schema.usuario_administrador:
        return unauthorized(
            detail='Você não tem permissão para atualizar esse recurso.'
        )

    update_data = update_schema.model_dump(exclude=['email_usuario'])

    for key, value in update_data.items():
        setattr(db_resource, key, value)

    db.commit()
    db.refresh(db_resource)
    return db_resource


def delete(delete_schema, resource_id:int, resource, db: Session, detail: str):
    db_resource = get(resource=resource, resource_id=resource_id, db=db, detail=detail)

    if db_resource.email_usuario != delete_schema.email_usuario\
        and not delete_schema.usuario_administrador:
        return unauthorized(
            detail="Você não tem permissão para deletar esse recurso."
        )

    if db_resource.cancelado:
        return not_found(detail=detail)

    if db_resource and db_resource.google_event_id:
       delete_calendar_event(db_resource.google_event_id)
       
       db_resource.cancelado = True
       db.commit()
       db.refresh(db_resource)
       return True

    return not_found(detail='Resource not found')
