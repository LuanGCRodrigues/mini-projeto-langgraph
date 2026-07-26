from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from app.db.session import get_db
from app.models.models import Cliente, Produto, Compra, ItemCompra
from app.schemas.schemas import (
    ClienteResponse,
    ClienteDetailResponse,
    ProdutoResponse,
    ProdutoDetailResponse,
    CompraResponse,
    CompraDetailResponse,
)

router = APIRouter(prefix="/api/v1", tags=["v1"])


# ============= CLIENTES =============

@router.get("/clientes", response_model=list[ClienteResponse])
def list_clientes(
    limite: int = Query(10, ge=1, le=100, alias="limit"),
    offset: int = Query(0, ge=0),
    cidade: Optional[str] = Query(None),
    estado: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Lista clientes com filtros opcionais por cidade e estado"""
    query = db.query(Cliente)
    
    if cidade:
        query = query.filter(Cliente.cidade.ilike(f"%{cidade}%"))
    if estado:
        query = query.filter(Cliente.estado.ilike(f"%{estado}%"))
    
    clientes = query.order_by(Cliente.id).offset(offset).limit(limite).all()
    return clientes


@router.get("/clientes/{cliente_id}", response_model=ClienteDetailResponse)
def get_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Retorna detalhes de um cliente específico"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    
    return cliente


# ============= PRODUTOS =============

@router.get("/produtos", response_model=list[ProdutoResponse])
def list_produtos(
    limite: int = Query(10, ge=1, le=100, alias="limit"),
    offset: int = Query(0, ge=0),
    categoria: Optional[str] = Query(None),
    ativo: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    """Lista produtos com filtros opcionais por categoria e status ativo"""
    query = db.query(Produto)
    
    if categoria:
        query = query.filter(Produto.categoria.ilike(f"%{categoria}%"))
    if ativo is not None:
        query = query.filter(Produto.ativo == ativo)
    
    produtos = query.order_by(Produto.id).offset(offset).limit(limite).all()
    return produtos


@router.get("/produtos/{produto_id}", response_model=ProdutoDetailResponse)
def get_produto(produto_id: int, db: Session = Depends(get_db)):
    """Retorna detalhes de um produto específico"""
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {produto_id} não encontrado"
        )
    
    return produto


# ============= COMPRAS =============

@router.get("/compras", response_model=list[CompraResponse])
def list_compras(
    limite: int = Query(10, ge=1, le=100, alias="limit"),
    offset: int = Query(0, ge=0),
    cliente_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    data_inicio: Optional[datetime] = Query(None),
    data_fim: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Lista compras com filtros opcionais por cliente, status e intervalo de datas"""
    query = db.query(Compra)
    
    if cliente_id:
        query = query.filter(Compra.cliente_id == cliente_id)
    if status:
        query = query.filter(Compra.status.ilike(f"%{status}%"))
    if data_inicio:
        query = query.filter(Compra.criada_em >= data_inicio)
    if data_fim:
        query = query.filter(Compra.criada_em <= data_fim)
    
    compras = query.order_by(desc(Compra.criada_em)).offset(offset).limit(limite).all()
    return compras


@router.get("/compras/{compra_id}", response_model=CompraDetailResponse)
def get_compra(compra_id: int, db: Session = Depends(get_db)):
    """Retorna detalhes completos de uma compra (cliente, itens e produtos)"""
    compra = db.query(Compra).filter(Compra.id == compra_id).first()
    
    if not compra:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Compra com ID {compra_id} não encontrada"
        )
    
    return compra
