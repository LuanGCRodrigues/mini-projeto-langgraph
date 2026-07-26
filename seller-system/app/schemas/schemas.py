from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator


class ClienteBase(BaseModel):
    nome: str
    email: str
    cidade: Optional[str] = None
    estado: Optional[str] = None


class ClienteResponse(ClienteBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True


class ClienteDetailResponse(ClienteResponse):
    """Schema detalhado para GET /clientes/{id}"""
    pass


class ProdutoBase(BaseModel):
    nome: str
    categoria: Optional[str] = None
    preco_unitario: float
    estoque: int = 0
    ativo: bool = True

    @field_validator('preco_unitario')
    @classmethod
    def preco_deve_ser_positivo(cls, v):
        if v <= 0:
            raise ValueError('Preço deve ser maior que zero')
        return v


class ProdutoResponse(ProdutoBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True


class ProdutoDetailResponse(ProdutoResponse):
    """Schema detalhado para GET /produtos/{id}"""
    pass


class ItemCompraBase(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: float
    subtotal: float

    @field_validator('quantidade')
    @classmethod
    def quantidade_deve_ser_positiva(cls, v):
        if v <= 0:
            raise ValueError('Quantidade deve ser maior que zero')
        return v


class ItemCompraResponse(ItemCompraBase):
    id: int
    compra_id: int

    class Config:
        from_attributes = True


class ItemCompraProdutoResponse(BaseModel):
    """Item compra com detalhes do produto"""
    id: int
    quantidade: int
    preco_unitario: float
    subtotal: float
    produto: 'ProdutoDetailResponse'

    class Config:
        from_attributes = True


class CompraBase(BaseModel):
    cliente_id: int
    status: str = "pendente"
    valor_total: float = 0.0

    @field_validator('status')
    @classmethod
    def status_valido(cls, v):
        status_validos = ['pendente', 'confirmada', 'enviada', 'entregue', 'cancelada']
        if v not in status_validos:
            raise ValueError(f'Status inválido. Deve ser um dos: {", ".join(status_validos)}')
        return v


class CompraResponse(CompraBase):
    id: int
    criada_em: datetime
    itens: list[ItemCompraResponse] = []

    class Config:
        from_attributes = True


class CompraDetailResponse(BaseModel):
    """Schema detalhado para GET /compras/{id}"""
    id: int
    cliente_id: int
    criada_em: datetime
    status: str
    valor_total: float
    cliente: ClienteResponse
    itens: list[ItemCompraProdutoResponse] = []

    class Config:
        from_attributes = True

