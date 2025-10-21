from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, registry, mapped_column
from itzn_api.db.base import tabela_registro

tabela_registro = registry()

@tabela_registro.mapped_as_dataclass
class agendamento:
    __tablename__ = 'agendamentos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    data_inicio: Mapped[datetime] = mapped_column(init=False, server_default=func.now)
    data_fim: Mapped[datetime] = mapped_column(init=False, server_default=func.now)
    computador: Mapped[int]
    email_usuario: Mapped[str] = mapped_column(unique=True, foreing_key=True)