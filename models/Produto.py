from dataclasses import dataclass
from typing import Optional

@dataclass
class Produto:
    id: Optional[int] = None
    nome: Optional[str] = None
    valor: Optional[float] = None
    desc: Optional[str] = None