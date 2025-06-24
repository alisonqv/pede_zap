from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import crud, schemas, models, database
from utils.gerar_pedido_imagem import gerar_imagem_pedido  # importa a função que gera a imagem
from datetime import datetime

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/pedidos/")
def criar_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    return crud.criar_pedido(db, pedido)

@router.put("/pedidos/{pedido_id}")
def editar_pedido(pedido_id: int, dados: schemas.PedidoCreate, db: Session = Depends(get_db)):
    pedido = db.query(models.Pedido).filter_by(id=pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if not crud.pode_editar_pedido(pedido):
        raise HTTPException(status_code=403, detail="O prazo de 5 minutos para editar expirou")

    # Apagar itens antigos
    db.query(models.ItemPedido).filter_by(pedido_id=pedido.id).delete()
    for item in dados.itens:
        db_item = models.ItemPedido(
            pedido_id=pedido.id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            observacao=item.observacao
        )
        db.add(db_item)
    db.commit()
    return db.query(models.Pedido).filter_by(id=pedido_id).first()

@router.put("/pedidos/{pedido_id}/confirmacao", response_model=schemas.Pedido)
def confirmar_pedido(pedido_id: int, dados: schemas.ConfirmacaoPedido, db: Session = Depends(get_db)):
    pedido = crud.confirmar_pedido(db, pedido_id, dados.confirmado)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    # Montar lista de itens para gerar imagem
    lista_de_itens_do_pedido = []
    for item in pedido.itens:
        lista_de_itens_do_pedido.append({
            "nome": item.produto.nome,
            "quantidade": item.quantidade,
            "preco": float(item.produto.preco),  # converter para float caso seja Decimal
            "categoria": item.produto.categoria,
            "observacao": item.observacao or ""
        })

    # Gerar imagem do pedido
    try:
        gerar_imagem_pedido(
            nome_restaurante="PITICUS CHURRASCARIA",
            numero_restaurante="(11) 9999-9999",
            nome_cliente=pedido.cliente_nome,
            telefone_cliente=pedido.cliente_numero,
            itens_pedido=lista_de_itens_do_pedido,
            caminho_salvar=f"pedidos/pedido_{pedido.id}.png"
        )
    except Exception as e:
        print(f"Erro ao gerar imagem do pedido: {e}")

    return pedido

@router.get("/pedidos/", response_model=List[schemas.Pedido])
def listar_pedidos(
    status: Optional[str] = Query(None),
    data_inicio: Optional[datetime] = Query(None),
    data_fim: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Pedido)

    if status:
        query = query.filter(models.Pedido.status == status)

    if data_inicio:
        query = query.filter(models.Pedido.criado_em >= data_inicio)

    if data_fim:
        query = query.filter(models.Pedido.criado_em <= data_fim)

    pedidos = query.order_by(models.Pedido.criado_em.desc()).all()
    return pedidos
