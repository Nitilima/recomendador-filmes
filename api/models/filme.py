from pydantic import BaseModel
from typing import Optional

class Filme(BaseModel):
    id: str
    nome: str
    ano: int
    genero: str
    avaliacao: float

class AtualizaFilme(BaseModel):
    nome: Optional[str] = None
    ano: Optional[int] = None
    genero: Optional[str] = None
    avaliacao: Optional[float] = None