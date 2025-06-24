from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def gerar_imagem_pedido(
    nome_restaurante: str,
    numero_restaurante: str,
    nome_cliente: str,
    telefone_cliente: str,
    itens_pedido: list,       # lista de dicts: {nome, quantidade, preco, categoria, observacao}
    caminho_salvar="pedido.png"
):
    # Configurações básicas
    largura = 600
    altura = 800
    fundo = "white"
    cor_texto = "black"

    # Fonte (usar fonte padrão do sistema, pode trocar depois)
    fonte_titulo = ImageFont.load_default()
    fonte_normal = ImageFont.load_default()

    # Criar imagem branca
    img = Image.new("RGB", (largura, altura), fundo)
    draw = ImageDraw.Draw(img)

    # Margens
    x = 20
    y = 20
    espacamento = 25

    # Linha 1: PEDIDO CONFIRMADO (centralizado)
    titulo = "-----PEDIDO CONFIRMADO-----"
    w, h = draw.textsize(titulo, font=fonte_titulo)
    draw.text(((largura - w) / 2, y), titulo, fill=cor_texto, font=fonte_titulo)
    y += espacamento * 2

    # Linha 2: Nome restaurante (esquerda) + data/hora (direita)
    datahora = datetime.now().strftime("%d/%m/%Y %H:%M")
    draw.text((x, y), nome_restaurante, fill=cor_texto, font=fonte_normal)
    w_data, _ = draw.textsize(datahora, font=fonte_normal)
    draw.text((largura - w_data - x, y), datahora, fill=cor_texto, font=fonte_normal)
    y += espacamento

    # Linha 3: Número do restaurante
    draw.text((x, y), f"Número: {numero_restaurante}", fill=cor_texto, font=fonte_normal)
    y += espacamento * 2

    # Dados do cliente
    draw.text((x, y), f"Cliente: {nome_cliente}", fill=cor_texto, font=fonte_normal)
    y += espacamento
    draw.text((x, y), f"Telefone: {telefone_cliente}", fill=cor_texto, font=fonte_normal)
    y += espacamento * 2

    # Dados do pedido (Separar bebidas dos demais)
    produtos = [item for item in itens_pedido if item.get("categoria") != "bebida"]
    bebidas = [item for item in itens_pedido if item.get("categoria") == "bebida"]

    def desenhar_lista(itens, titulo_secao):
        nonlocal y
        if not itens:
            return
        draw.text((x, y), titulo_secao, fill=cor_texto, font=fonte_normal)
        y += espacamento
        total = 0
        for item in itens:
            nome = item.get("nome", "")
            qtd = item.get("quantidade", 1)
            preco = item.get("preco", 0)
            obs = item.get("observacao", "")
            linha = f"{qtd}x {nome} - R$ {preco:.2f}"
            draw.text((x + 10, y), linha, fill=cor_texto, font=fonte_normal)
            y += espacamento
            if obs:
                draw.text((x + 30, y), f"Obs: {obs}", fill=cor_texto, font=fonte_normal)
                y += espacamento
            total += preco * qtd
        y += espacamento
        draw.text((x + 10, y), f"Subtotal: R$ {total:.2f}", fill=cor_texto, font=fonte_normal)
        y += espacamento * 2

    desenhar_lista(produtos, "Produtos:")
    desenhar_lista(bebidas, "Bebidas:")

    # Rodapé
    rodape = "Agradecemos pela preferência!!!"
    w, _ = draw.textsize(rodape, font=fonte_normal)
    draw.text(((largura - w) / 2, altura - espacamento * 2), rodape, fill=cor_texto, font=fonte_normal)

    # Salvar imagem
    img.save(caminho_salvar)
    print(f"Imagem do pedido salva em {caminho_salvar}")