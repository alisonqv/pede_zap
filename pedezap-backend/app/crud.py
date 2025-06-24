from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from . import models, schemas
from utils.gerar_pedido_imagem import gerar_imagem_pedido

def criar_pedido(db: Session, pedido: schemas.PedidoCreate):
    novo = models.Pedido(
        restaurante_id=pedido.restaurante_id,
        cliente_nome=pedido.cliente_nome,
        cliente_numero=pedido.cliente_numero
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)

    # Adiciona os itens do pedido
    for item in pedido.itens:
        db_item = models.ItemPedido(
            pedido_id=novo.id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            observacao=item.observacao
        )
        db.add(db_item)
    db.commit()

    # Recarrega os itens para montar lista_de_itens_do_pedido
    db.refresh(novo)  # para garantir que o novo está atualizado com relacionamento

    lista_de_itens_do_pedido = []
    for item in novo.itens:
        lista_de_itens_do_pedido.append({
            "nome": item.produto.nome,
            "quantidade": item.quantidade,
            "preco": float(item.produto.preco),
            "categoria": item.produto.categoria,
            "observacao": item.observacao or ""
        })

    # Gera imagem do pedido
    gerar_imagem_pedido(
        nome_restaurante="Seu Restaurante",
        numero_restaurante="(11) 9999-9999",
        nome_cliente=novo.cliente_nome,
        telefone_cliente=novo.cliente_numero,
        itens_pedido=lista_de_itens_do_pedido,
        caminho_salvar=f"pedidos/pedido_{novo.id}.png"
    )

    return novo

def confirmar_pedido(db: Session, pedido_id: int, confirmado: bool):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if not pedido:
        return None
    pedido.status = "confirmado" if confirmado else "cancelado"
    db.commit()
    db.refresh(pedido)
    return pedido

def pode_editar_pedido(pedido: models.Pedido):
    return datetime.now(timezone.utc) - pedido.criado_em <= timedelta(minutes=5)
