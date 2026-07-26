from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, func
from app.db.session import get_db
from app.models.models import Cliente, Produto, Compra, ItemCompra
from app.schemas.schemas import (
    ClienteResponse,
    ClienteDetailResponse,
    ProdutoResponse,
    ProdutoDetailResponse,
    CompraResponse,
    CompraDetailResponse,
    RelatorioClienteResponse,
    RelatorioProdutosMaisVendidosResponse,
    RelatorioResumoComprasResponse,
    RelatorioEstoqueBaixoResponse
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


# ============= RELATÓRIOS =============

@router.get("/relatorios/clientes/{cliente_id}", response_model=RelatorioClienteResponse)
def relatorio_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Retorna um resumo detalhado de um cliente específico"""
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente {cliente_id} não encontrado")

    # Agregações de compras
    resumo_compras = db.query(
        func.count(Compra.id).label("total_compras"),
        func.sum(Compra.valor_total).label("valor_total"),
        func.max(Compra.criada_em).label("ultima_compra")
    ).filter(Compra.cliente_id == cliente_id, Compra.status != "cancelada").first()

    # Produtos mais comprados
    produtos_query = db.query(
        Produto.id,
        Produto.nome,
        func.sum(ItemCompra.quantidade).label("total_qtd")
    ).join(ItemCompra).join(Compra).filter(
        Compra.cliente_id == cliente_id,
        Compra.status != "cancelada"
    ).group_by(Produto.id).order_by(desc("total_qtd")).limit(5).all()

    return {
        "cliente": cliente,
        "total_compras": resumo_compras.total_compras or 0,
        "valor_total_gasto": resumo_compras.valor_total or 0.0,
        "ultima_compra_em": resumo_compras.ultima_compra,
        "produtos_mais_comprados": [
            {"id": p.id, "nome": p.nome, "quantidade_comprada": p.total_qtd}
            for p in produtos_query
        ]
    }


@router.get("/relatorios/produtos-mais-vendidos", response_model=RelatorioProdutosMaisVendidosResponse)
def relatorio_produtos_mais_vendidos(
    data_inicio: Optional[datetime] = Query(None),
    data_fim: Optional[datetime] = Query(None),
    limite: int = Query(10, ge=1, le=50, alias="limit"),
    db: Session = Depends(get_db)
):
    """Lista os produtos mais vendidos em um período"""
    query = db.query(
        Produto.id,
        Produto.nome,
        func.sum(ItemCompra.quantidade).label("total_qtd"),
        func.sum(ItemCompra.subtotal).label("receita")
    ).join(ItemCompra).join(Compra).filter(Compra.status != "cancelada")

    if data_inicio:
        query = query.filter(Compra.criada_em >= data_inicio)
    if data_fim:
        query = query.filter(Compra.criada_em <= data_fim)

    resultados = query.group_by(Produto.id).order_by(desc("total_qtd")).limit(limite).all()

    return {
        "periodo": {"inicio": data_inicio, "fim": data_fim},
        "produtos": [
            {
                "produto_id": r.id,
                "nome": r.nome,
                "quantidade_vendida": r.total_qtd,
                "receita_total": r.receita
            } for r in resultados
        ]
    }


@router.get("/relatorios/resumo-compras", response_model=RelatorioResumoComprasResponse)
def relatorio_resumo_compras(
    data_inicio: Optional[datetime] = Query(None),
    data_fim: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Resumo geral de vendas em um período"""
    query = db.query(
        func.count(Compra.id).label("total"),
        func.sum(Compra.valor_total).label("receita")
    ).filter(Compra.status != "cancelada")

    if data_inicio:
        query = query.filter(Compra.criada_em >= data_inicio)
    if data_fim:
        query = query.filter(Compra.criada_em <= data_fim)

    resumo = query.first()
    total = resumo.total or 0
    receita = resumo.receita or 0.0
    ticket = receita / total if total > 0 else 0.0

    return {
        "periodo": {"inicio": data_inicio, "fim": data_fim},
        "quantidade_total": total,
        "receita_total": receita,
        "ticket_medio": ticket
    }


@router.get("/relatorios/estoque-baixo", response_model=list[RelatorioEstoqueBaixoResponse])
def relatorio_estoque_baixo(
    limite_estoque: int = Query(5, ge=0),
    db: Session = Depends(get_db)
):
    """Lista produtos ativos com estoque abaixo do limite informado"""
    produtos = db.query(Produto).filter(
        Produto.ativo == True,
        Produto.estoque <= limite_estoque
    ).order_by(Produto.estoque).all()

    return [
        {
            "id": p.id,
            "nome": p.nome,
            "categoria": p.categoria,
            "estoque_atual": p.estoque,
            "preco_unitario": p.preco_unitario
        } for p in produtos
    ]
