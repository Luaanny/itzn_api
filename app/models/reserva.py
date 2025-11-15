from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, registry, mapped_column 
from app.db.base import tabela_registro

@tabela_registro.mapped_as_dataclass()
class Reserva:
    __tablename__ = 'reservas'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    data_reserva: Mapped[date] = mapped_column(nullable=False)
    justificativa: Mapped[str]
    email_usuario: Mapped[str] = mapped_column(String(50), nullable=False)