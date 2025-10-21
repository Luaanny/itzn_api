from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, registry, mapped_column 
from app.db.base import tabela_registro

tabela_registro = registry()

@tabela_registro.mapped_as_dataclass
class reserva:
    __tablename__ = 'reservas'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    data_inicio: Mapped[datetime] = mapped_column(init=False, server_default=func.now)
    data_fim: Mapped[datetime] = mapped_column(init=False, server_default=func.now)
    justificativa: Mapped[str]
    email_usuario: Mapped[str] = mapped_column(unique=True, foreign_key=True)