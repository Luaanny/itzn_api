from datetime import datetime
from sqlalchemy import Mapped, registry 
from itzn_api.db.base import tabela_registro

tabela_registro = registry()

@tabela_registro.mapped_as_dataclass
class user:
    __tablename__ = 'users'

    email_usuario: Mapped[str] = mapped_column(init=False, primary_key=True)
    cargo_usuario: Mapped[str]