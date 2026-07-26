"""Initial migration: create tables with seed data

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from datetime import datetime

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'clientes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('cidade', sa.String(100)),
        sa.Column('estado', sa.String(2)),
        sa.Column('criado_em', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'produtos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(255), nullable=False),
        sa.Column('categoria', sa.String(100)),
        sa.Column('preco_unitario', sa.Float(), nullable=False),
        sa.Column('estoque', sa.Integer(), nullable=False),
        sa.Column('ativo', sa.Boolean(), nullable=False),
        sa.Column('criado_em', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'compras',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cliente_id', sa.Integer(), nullable=False),
        sa.Column('criada_em', sa.DateTime(), nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('valor_total', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['cliente_id'], ['clientes.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'itens_compra',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('compra_id', sa.Integer(), nullable=False),
        sa.Column('produto_id', sa.Integer(), nullable=False),
        sa.Column('quantidade', sa.Integer(), nullable=False),
        sa.Column('preco_unitario', sa.Float(), nullable=False),
        sa.Column('subtotal', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['compra_id'], ['compras.id'], ),
        sa.ForeignKeyConstraint(['produto_id'], ['produtos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Insert seed data
    op.execute(text(
        "INSERT INTO clientes (id, nome, email, cidade, estado, criado_em) VALUES "
        "(1, 'João Silva', 'joao@example.com', 'São Paulo', 'SP', '2024-01-01 00:00:00'), "
        "(2, 'Maria Santos', 'maria@example.com', 'Rio de Janeiro', 'RJ', '2024-01-01 00:00:00'), "
        "(3, 'Pedro Oliveira', 'pedro@example.com', 'Belo Horizonte', 'MG', '2024-01-01 00:00:00'), "
        "(4, 'Ana Costa', 'ana@example.com', 'Salvador', 'BA', '2024-01-01 00:00:00'), "
        "(5, 'Carlos Ferreira', 'carlos@example.com', 'Fortaleza', 'CE', '2024-01-01 00:00:00'), "
        "(6, 'Lucia Gomes', 'lucia@example.com', 'Curitiba', 'PR', '2024-01-01 00:00:00'), "
        "(7, 'Roberto Mendes', 'roberto@example.com', 'Recife', 'PE', '2024-01-01 00:00:00'), "
        "(8, 'Fernanda Lima', 'fernanda@example.com', 'Brasília', 'DF', '2024-01-01 00:00:00'), "
        "(9, 'Bruno Alves', 'bruno@example.com', 'Manaus', 'AM', '2024-01-01 00:00:00'), "
        "(10, 'Patricia Rocha', 'patricia@example.com', 'Belém', 'PA', '2024-01-01 00:00:00')"
    ))

    op.execute(text(
        "INSERT INTO produtos (id, nome, categoria, preco_unitario, estoque, ativo, criado_em) VALUES "
        "(1, 'Notebook Dell', 'Eletrônicos', 3500.00, 10, 1, '2024-01-01 00:00:00'), "
        "(2, 'Mouse Logitech', 'Periféricos', 85.50, 50, 1, '2024-01-01 00:00:00'), "
        "(3, 'Teclado Mecânico', 'Periféricos', 450.00, 30, 1, '2024-01-01 00:00:00'), "
        "(4, 'Monitor LG 27\"', 'Monitores', 1200.00, 15, 1, '2024-01-01 00:00:00'), "
        "(5, 'Webcam Razer', 'Periféricos', 300.00, 20, 1, '2024-01-01 00:00:00'), "
        "(6, 'Headset Sony', 'Áudio', 750.00, 25, 1, '2024-01-01 00:00:00'), "
        "(7, 'SSD Samsung 1TB', 'Armazenamento', 450.00, 40, 1, '2024-01-01 00:00:00'), "
        "(8, 'Memória RAM 16GB', 'Componentes', 250.00, 60, 1, '2024-01-01 00:00:00'), "
        "(9, 'Processador Intel', 'Componentes', 1500.00, 12, 1, '2024-01-01 00:00:00'), "
        "(10, 'Placa Mãe Asus', 'Componentes', 800.00, 18, 1, '2024-01-01 00:00:00'), "
        "(11, 'Fonte 750W', 'Componentes', 350.00, 22, 1, '2024-01-01 00:00:00'), "
        "(12, 'Gabinete Corsair', 'Componentes', 400.00, 16, 1, '2024-01-01 00:00:00'), "
        "(13, 'Mousepad Gamer', 'Periféricos', 120.00, 35, 1, '2024-01-01 00:00:00'), "
        "(14, 'Câmera Digital', 'Fotografia', 2200.00, 8, 1, '2024-01-01 00:00:00'), "
        "(15, 'Roteador WiFi', 'Redes', 280.00, 28, 1, '2024-01-01 00:00:00')"
    ))

    op.execute(text(
        "INSERT INTO compras (id, cliente_id, criada_em, status, valor_total) VALUES "
        "(1, 1, '2024-01-01 00:00:00', 'entregue', 3671.00), "
        "(2, 2, '2024-01-01 00:00:00', 'entregue', 1650.00), "
        "(3, 3, '2024-01-01 00:00:00', 'pendente', 300.00), "
        "(4, 4, '2024-01-01 00:00:00', 'entregue', 1950.00), "
        "(5, 5, '2024-01-01 00:00:00', 'pendente', 1750.00), "
        "(6, 6, '2024-01-01 00:00:00', 'entregue', 1600.00), "
        "(7, 7, '2024-01-01 00:00:00', 'entregue', 750.00), "
        "(8, 8, '2024-01-01 00:00:00', 'pendente', 360.00), "
        "(9, 9, '2024-01-01 00:00:00', 'entregue', 2200.00), "
        "(10, 10, '2024-01-01 00:00:00', 'entregue', 3780.00), "
        "(11, 1, '2024-01-01 00:00:00', 'entregue', 877.50), "
        "(12, 2, '2024-01-01 00:00:00', 'pendente', 2400.00), "
        "(13, 3, '2024-01-01 00:00:00', 'entregue', 1350.00), "
        "(14, 4, '2024-01-01 00:00:00', 'entregue', 1400.00), "
        "(15, 5, '2024-01-01 00:00:00', 'pendente', 2300.00), "
        "(16, 6, '2024-01-01 00:00:00', 'entregue', 700.00), "
        "(17, 7, '2024-01-01 00:00:00', 'entregue', 640.00), "
        "(18, 8, '2024-01-01 00:00:00', 'pendente', 2760.00), "
        "(19, 9, '2024-01-01 00:00:00', 'entregue', 3585.50), "
        "(20, 10, '2024-01-01 00:00:00', 'entregue', 2100.00)"
    ))

    op.execute(text(
        "INSERT INTO itens_compra (id, compra_id, produto_id, quantidade, preco_unitario, subtotal) VALUES "
        "(11, 1, 1, 1, 3500.00, 3500.00), (12, 1, 2, 2, 85.50, 171.00), "
        "(21, 2, 3, 1, 450.00, 450.00), (22, 2, 4, 1, 1200.00, 1200.00), "
        "(31, 3, 5, 1, 300.00, 300.00), "
        "(41, 4, 6, 2, 750.00, 1500.00), (42, 4, 7, 1, 450.00, 450.00), "
        "(51, 5, 8, 1, 250.00, 250.00), (52, 5, 9, 1, 1500.00, 1500.00), "
        "(61, 6, 10, 2, 800.00, 1600.00), "
        "(71, 7, 11, 1, 350.00, 350.00), (72, 7, 12, 1, 400.00, 400.00), "
        "(81, 8, 13, 3, 120.00, 360.00), "
        "(91, 9, 14, 1, 2200.00, 2200.00), "
        "(101, 10, 15, 1, 280.00, 280.00), (102, 10, 1, 1, 3500.00, 3500.00), "
        "(111, 11, 2, 5, 85.50, 427.50), (112, 11, 3, 1, 450.00, 450.00), "
        "(121, 12, 4, 2, 1200.00, 2400.00), "
        "(131, 13, 5, 2, 300.00, 600.00), (132, 13, 6, 1, 750.00, 750.00), "
        "(141, 14, 7, 2, 450.00, 900.00), (142, 14, 8, 2, 250.00, 500.00), "
        "(151, 15, 9, 1, 1500.00, 1500.00), (152, 15, 10, 1, 800.00, 800.00), "
        "(161, 16, 11, 2, 350.00, 700.00), "
        "(171, 17, 12, 1, 400.00, 400.00), (172, 17, 13, 2, 120.00, 240.00), "
        "(181, 18, 14, 1, 2200.00, 2200.00), (182, 18, 15, 2, 280.00, 560.00), "
        "(191, 19, 1, 1, 3500.00, 3500.00), (192, 19, 2, 1, 85.50, 85.50), "
        "(201, 20, 3, 2, 450.00, 900.00), (202, 20, 4, 1, 1200.00, 1200.00)"
    ))


def downgrade() -> None:
    op.drop_table('itens_compra')
    op.drop_table('compras')
    op.drop_table('produtos')
    op.drop_table('clientes')
