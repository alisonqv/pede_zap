from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    restaurante_id = Column(Integer, nullable=False)
    cliente_nome = Column(String)
    cliente_numero = Column(String)
    forma_pagamento = Column(String)  # <-- NOVO CAMPO
    status = Column(String, default="pendente")
    imagem_pedido = Column(Text)
    criado_em = Column(DateTime, default=datetime.utcnow)

    itens = relationship("ItemPedido", back_populates="pedido")

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer, default=1)
    observacao = Column(Text)

    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto")  # <-- RELACIONAMENTO PARA OBTER DETALHES
