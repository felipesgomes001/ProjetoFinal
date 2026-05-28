import streamlit as st
import socket

st.title("🚗 Rover Control Panel")

# ── CSS para destacar botão ativo ────────────────────────────
st.markdown("""
<style>
.botao-ativo {
    background-color: #00cc44 !important;
    color: white !important;
    font-size: 1.4em;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
    font-weight: bold;
    border: 3px solid #00ff55;
    box-shadow: 0 0 12px #00cc44;
}
.botao-inativo {
    background-color: #2e2e2e;
    color: #aaaaaa;
    font-size: 1.4em;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
    border: 2px solid #444;
}
</style>
""", unsafe_allow_html=True)

# ── Configuração de conexão ──────────────────────────────────
ip = st.text_input("IP do Rover", value="192.168.7.149")
porta = st.number_input("Porta", value=5000, step=1)

if "cliente" not in st.session_state:
    st.session_state.cliente = None

if "cmd_ativo" not in st.session_state:
    st.session_state.cmd_ativo = None  # qual botão está destacado

col1, col2 = st.columns(2)
with col1:
    if st.button("🔌 Conectar"):
        try:
            cliente = socket.socket()
            cliente.connect((ip, int(porta)))
            st.session_state.cliente = cliente
            st.success("Conectado!")
        except Exception as e:
            st.error(f"Erro ao conectar: {e}")

with col2:
    if st.button("❌ Desconectar"):
        if st.session_state.cliente:
            st.session_state.cliente.close()
            st.session_state.cliente = None
            st.info("Desconectado.")

# ── Função para enviar e marcar botão ativo ──────────────────
def enviar(cmd: bytes, nome: str):
    st.session_state.cmd_ativo = nome
    try:
        if st.session_state.cliente:
            st.session_state.cliente.send(cmd)
        else:
            st.warning("Conecte-se primeiro!")
    except Exception as e:
        st.error(f"Erro ao enviar: {e}")

# ── Função para renderizar botão visual ──────────────────────
def botao_visual(label, cmd, nome, col):
    ativo = st.session_state.cmd_ativo == nome
    classe = "botao-ativo" if ativo else "botao-inativo"
    col.markdown(f'<div class="{classe}">{label}</div>', unsafe_allow_html=True)
    if col.button(f"{nome}", key=f"btn_{nome}", use_container_width=True):
        enviar(cmd, nome)

# ── Layout de controle ───────────────────────────────────────
st.divider()
st.subheader("Controle")

# Linha: Frente
c1, c2, c3 = st.columns([1, 1, 1])
botao_visual("⬆️ Frente", b"w", "W", c2)

# Linha: Esquerda | Parar | Direita
c4, c5, c6 = st.columns([1, 1, 1])
botao_visual("⬅️ Esq", b"a", "A", c4)
botao_visual("⏹️ Parar", b"p", "P", c5)
botao_visual("➡️ Dir", b"d", "D", c6)

# Linha: Trás
c7, c8, c9 = st.columns([1, 1, 1])
botao_visual("⬇️ Trás", b"s", "S", c8)

# ── Status ───────────────────────────────────────────────────
st.divider()
if st.session_state.cliente:
    st.success(f"✅ Conectado em {ip}:{int(porta)}")
else:
    st.warning("⚠️ Desconectado")