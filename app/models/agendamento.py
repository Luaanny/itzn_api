from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import tabela_registro

@tabela_registro.mapped_as_dataclass()
class Agendamento:
    __tablename__ = 'agendamentos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    data_agendamento: Mapped[date] = mapped_column(nullable=False)
    hora_inicio: Mapped[int] = mapped_column(nullable=False)
    numero_computador: Mapped[int]
    email_usuario: Mapped[str] = mapped_column(String(50), nullable=False)