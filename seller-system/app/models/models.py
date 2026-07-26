from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    cidade = Column(String(100))
    estado = Column(String(2))
    criado_em = Column(DateTime, default=datetime.utcnow)

    compras = relationship("Compra", back_populates="cliente", cascade="all, delete-orphan")


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    categoria = Column(String(100))
    preco_unitario = Column(Float, nullable=False)
    estoque = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

    itens_compra = relationship("ItemCompra", back_populates="produto")


class Compra(Base):
    __tablename__ = "compras"

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    criada_em = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="pendente")
    valor_total = Column(Float, default=0.0)

    cliente = relationship("Cliente", back_populates="compras")
    itens = relationship("ItemCompra", back_populates="compra", cascade="all, delete-orphan")


class ItemCompra(Base):
    __tablename__ = "itens_compra"

    id = Column(Integer, primary_key=True)
    compra_id = Column(Integer, ForeignKey("compras.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    compra = relationship("Compra", back_populates="itens")
    produto = relationship("Produto", back_populates="itens_compra")
