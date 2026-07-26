from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.session import get_db
from app.models.models import Cliente, Produto, Compra
from app.schemas.schemas import ClienteResponse, ProdutoResponse, CompraResponse

router = APIRouter(prefix="/api/v1", tags=["v1"])


@router.get("/clientes", response_model=list[ClienteResponse])
def list_clientes(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    clientes = db.query(Cliente).order_by(Cliente.id).offset(offset).limit(limit).all()
    return clientes


@router.get("/produtos", response_model=list[ProdutoResponse])
def list_produtos(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    produtos = db.query(Produto).order_by(Produto.id).offset(offset).limit(limit).all()
    return produtos


@router.get("/compras", response_model=list[CompraResponse])
def list_compras(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    compras = db.query(Compra).order_by(Compra.id).offset(offset).limit(limit).all()
    return compras
