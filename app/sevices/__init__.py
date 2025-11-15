from sqlalchemy.orm import Session
from app.core.exceptions import not_found, conflict, unauthorized
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models.reserva import Reserva
from app.models.agendamento import Agendamento


def get_resources(resource: Reserva | Agendamento, db: Session, detail: str = 'Not found'):
    db_resource = db.scalars(select(resource)).all()
    return db_resource if db_resource else not_found(detail)


def get(resource: Reserva | Agendamento, db: Session, user_email: str, detail: str = 'Not found'):
    db_resource = db.scalar(select(resource).where(resource.email_usuario == user_email))

    return db_resource if db_resource else not_found(detail)


def get_all_user_resources(resource: Reserva | Agendamento, db: Session,
                           user_email: str, detail: str):
    db_resources = db.scalars(select(resource).where(resource.email_usuario == user_email)).all()

    return db_resources if db_resources else not_found(detail)


def post(resource: Reserva | Agendamento, create_schema, db: Session):
    resource_dict = create_schema.model_dump()
    db_resource = resource(**resource_dict)

    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)

    return db_resource


def put(update_schema, user_email: str, resource: Reserva | Agendamento, db: Session, detail):
    db_resource = get(resource=resource, user_email=user_email, db=db)

    update_data = update_schema.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_resource, key, value)

    db.commit()
    db.refresh(db_resource)
    return db_resource


def delete(user_email: str, resource, db: Session, detail: str):
    db_resource = get(resource=resource, user_email=user_email, db=db, detail=detail)

    if db_resource:
        db.delete(db_resource)
        db.commit()
        return True

    return not_found(detail='Resource not found')
