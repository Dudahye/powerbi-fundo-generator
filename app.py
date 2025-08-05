
# ✅ Autenticação do ngrok
from pyngrok import ngrok
ngrok.set_auth_token("30qIq7Tg3n7tLN9JQ8CBKv5JiuB_7T3WAnTJh33BeHqDG3iWo")  # ⬅️ Substitua pelo seu token se quiser

# ✅ Código do app salvo como app.py
code = """
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageColor
import os

st.set_page_config(layout="wide", page_title="Gerador de Fundos Power BI")
st.title("🧩 Criador de Fundo Personalizado para Power BI")

col_config, col_preview = st.columns([1, 1])

with col_config:
    largura = st.number_input("📏 Largura da Imagem", 800, 4000, 1280, step=10)
    altura = st.number_input("📐 Altura da Imagem", 600, 3000, 720, step=10)
    cor_fundo_inicio = st.color_picker("🎨 Cor Inicial do Fundo", "#0b2c44")
    cor_fundo_fim = st.color_picker("🎨 Cor Final do Fundo", "#1f4b99")
    cor_card = st.color_picker("⬜ Cor dos Cards", "#fdfdfd")
    cor_titulo = st.color_picker("🖍️ Cor do Título do Painel", "#ffffff")
    cor_titulo_card = st.color_picker("🖍️ Cor dos Títulos dos Cards", "#000000")

    espaco_horizontal = st.slider("↔️ Espaçamento Horizontal entre Cards", 0, 100, 30)
    espaco_vertical = st.slider("↕️ Espaçamento Vertical entre Linhas", 0, 100, 40)

    tamanho_titulo = st.slider("🔠 Tamanho da Fonte do Título", 20, 100, 38)
    tamanho_card_texto = st.slider("🔤 Tamanho da Fonte dos Cards", 10, 50, 18)
    titulo_painel = st.text_input("📋 Título do Painel", "Limites - Insira o título")

    fontes_disponiveis = {
      
        "Liberation Sans": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
    }
    fonte_escolhida = st.selectbox("✒️ Fonte", list(fontes_disponiveis.keys()), index=0)

    n_linhas = st.slider("🔢 Número de Linhas", 1, 5, 3)
    cards_config = []

    for i in range(n_linhas):
        st.markdown(f"#### Linha {i+1}")
        mesma_largura = st.checkbox(f"➡️ Todos os Cards da Linha {i+1} com a mesma largura", key=f"check_larg_{i}")
        mesma_altura = st.checkbox(f"⬇️ Todos os Cards da Linha {i+1} com a mesma altura", key=f"check_alt_{i}")
        n_cards = st.slider(f"Número de Cards na Linha {i+1}", 1, 5, 3, key=f"linha_{i}_n_cards")

        largura_comum = st.number_input(f"Largura comum para os Cards da Linha {i+1}", 100, 1000, 300, step=10, key=f"larg_comum_{i}") if mesma_largura else None
        altura_comum = st.number_input(f"Altura comum para os Cards da Linha {i+1}", 100, 1000, 200, step=10, key=f"alt_comum_{i}") if mesma_altura else None

        linha = []
        for j in range(n_cards):
            col1, col2, col3 = st.columns(3)
            with col1:
                largura_card = largura_comum if mesma_largura else st.number_input(f"Largura do Card {j+1}", 100, 1000, 300, step=10, key=f"larg_{i}_{j}")
            with col2:
                altura_card = altura_comum if mesma_altura else st.number_input(f"Altura do Card {j+1}", 100, 1000, 200, step=10, key=f"alt_{i}_{j}")
            with col3:
                titulo_card = st.text_input(f"Título do Card {j+1}", f"Card {j+1}", key=f"title_{i}_{j}")
            linha.append({
                "largura": largura_card,
                "altura": altura_card,
                "titulo": titulo_card
            })
        cards_config.append(linha)

def gerar_imagem():
    img = Image.new("RGB", (largura, altura), color=cor_fundo_inicio)
    draw = ImageDraw.Draw(img)

    for y in range(altura):
        r1, g1, b1 = ImageColor.getrgb(cor_fundo_inicio)
        r2, g2, b2 = ImageColor.getrgb(cor_fundo_fim)
        r = r1 + (r2 - r1) * y // altura
        g = g1 + (g2 - g1) * y // altura
        b = b1 + (b2 - b1) * y // altura
        draw.line([(0, y), (largura, y)], fill=(r, g, b))

    try:
        path_fonte = fontes_disponiveis[fonte_escolhida]
        fonte_titulo = ImageFont.truetype(path_fonte, tamanho_titulo)
        fonte_card = ImageFont.truetype(path_fonte, tamanho_card_texto)
    except:
        fonte_titulo = ImageFont.load_default()
        fonte_card = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), titulo_painel, font=fonte_titulo)
    largura_texto = bbox[2] - bbox[0]
    altura_texto = bbox[3] - bbox[1]
    draw.text(((largura - largura_texto) / 2, 30), titulo_painel, font=fonte_titulo, fill=cor_titulo)

    y_atual = 100 + altura_texto
    for linha in cards_config:
        total_largura = sum(card["largura"] for card in linha)
        espacamento_x = espaco_horizontal if len(linha) > 1 else 0
        x_atual = 50
        for card in linha:
            x0 = x_atual
            y0 = y_atual
            x1 = x0 + card["largura"]
            y1 = y0 + card["altura"]
            draw.rounded_rectangle([x0, y0, x1, y1], radius=20, fill=cor_card)
            draw.text((x0 + 10, y0 + 10), card["titulo"], font=fonte_card, fill=cor_titulo_card)
            x_atual = x1 + espacamento_x
        y_atual = y1 + espaco_vertical

    return img

with col_preview:
    st.markdown("### 📷 Pré-visualização")
    img_preview = gerar_imagem()
    st.image(img_preview, use_container_width=True)

if st.button("🚀 Gerar e Baixar Imagem Final"):
    output_path = "/mnt/data/fundo_powerbi_customizado.png"
    os.makedirs("/mnt/data", exist_ok=True)
    img_preview.save(output_path)
    st.success("✅ Imagem gerada com sucesso!")
    st.download_button("📥 Baixar imagem", data=open(output_path, "rb"), file_name="fundo_powerbi_customizado.png")
"""

with open("app.py", "w") as f:
    f.write(code)

# ✅ Roda o Streamlit com ngrok
public_url = ngrok.connect(8501)
print(f"🌐 Acesse o app aqui: {public_url}")
!streamlit run app.py & sleep 3
