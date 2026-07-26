from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class ClienteBase(BaseModel):
    nome: str
    email: EmailStr
    cidade: Optional[str] = None
    estado: Optional[str] = None


class ClienteResponse(ClienteBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True


class ProdutoBase(BaseModel):
    nome: str
    categoria: Optional[str] = None
    preco_unitario: float
    estoque: int = 0
    ativo: bool = True


class ProdutoResponse(ProdutoBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True


class ItemCompraBase(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: float
    subtotal: float


class ItemCompraResponse(ItemCompraBase):
    id: int
    compra_id: int

    class Config:
        from_attributes = True


class CompraBase(BaseModel):
    cliente_id: int
    status: str = "pendente"
    valor_total: float = 0.0


class CompraResponse(CompraBase):
    id: int
    criada_em: datetime
    itens: list[ItemCompraResponse] = []

    class Config:
        from_attributes = True
