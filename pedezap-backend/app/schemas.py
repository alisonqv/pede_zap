from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# -----------------------------
# Confirmação do pedido
# -----------------------------
class ConfirmacaoPedido(BaseModel):
    confirmado: bool

# -----------------------------
# Produto dentro do item do pedido
# -----------------------------
class ProdutoInfo(BaseModel):
    nome: str
    preco: float
    categoria: Optional[str]

    class Config:
        orm_mode = True

# -----------------------------
# ItemPedido - Criação e Resposta
# -----------------------------
class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int
    observacao: Optional[str] = None

class ItemPedidoResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    observacao: Optional[str]
    produto: ProdutoInfo  # detalhes do produto aninhado

    class Config:
        orm_mode = True

# -----------------------------
# Pedido - Criação e Resposta
# -----------------------------
class PedidoCreate(BaseModel):
    restaurante_id: int
    cliente_nome: Optional[str] = None
    cliente_numero: Optional[str] = None
    forma_pagamento: Optional[str] = None  # novo campo
    itens: List[ItemPedidoCreate]

class Pedido(BaseModel):
    id: int
    restaurante_id: int
    cliente_nome: Optional[str]
    cliente_numero: Optional[str]
    status: str
    forma_pagamento: Optional[str]
    imagem_pedido: Optional[str]
    criado_em: datetime
    itens: List[ItemPedidoResponse]

    class Config:
        orm_mode = True
