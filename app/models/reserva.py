from datetime import date

from sqlalchemy import String, Boolean
from sqlalchemy.sql import expression
from sqlalchemy.orm import Mapped,mapped_column 
from app.db.base import tabela_registro

@tabela_registro.mapped_as_dataclass()
class Reserva:
    __tablename__ = 'reservas'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    data_reserva: Mapped[date] = mapped_column(nullable=False)
    justificativa: Mapped[str]
    email_usuario: Mapped[str] = mapped_column(String(50), nullable=False)
    autor: Mapped[str] = mapped_column(String(50), nullable=False)
    google_event_id: Mapped[str | None] = mapped_column(String(255), nullable=True, init=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False,
                                        server_default='Aguardando Validação', init=False)
    alterado: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False,
                                          init=False, server_default=expression.false())
    alterado_por: Mapped[str] = mapped_column(String(50), nullable=True, init=False)
    cancelado: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False,
                                            init=False, server_default=expression.false())