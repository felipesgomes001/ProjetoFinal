# ============================================================
# menu.py — Painel web de controle do Rover (tudo em um)
# Controle via botões na interface web, sem pygame
# ============================================================

import streamlit as st
import socket

st.title("🚗 Rover Control Panel")

# ── Configuração de conexão ──────────────────────────────────
ip = st.text_input("IP do Rover", value="192.168.7.149")
porta = st.number_input("Porta", value=5000, step=1)

# ── Gerencia conexão no session_state ───────────────────────
if "cliente" not in st.session_state:
    st.session_state.cliente = None

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

# ── Função para enviar comando ───────────────────────────────
def enviar(cmd: bytes):
    try:
        if st.session_state.cliente:
            st.session_state.cliente.send(cmd)
        else:
            st.warning("Conecte-se primeiro!")
    except Exception as e:
        st.error(f"Erro ao enviar: {e}")

# ── Botões de controle ───────────────────────────────────────
st.divider()
st.subheader("Controle")

# Frente
col_esp, col_w, col_esp2 = st.columns([1, 1, 1])
with col_w:
    if st.button("⬆️ W — Frente", use_container_width=True):
        enviar(b"w")

# Esquerda | Parar | Direita
col_a, col_p, col_d = st.columns(3)
with col_a:
    if st.button("⬅️ A — Esq", use_container_width=True):
        enviar(b"a")
with col_p:
    if st.button("⏹️ Parar", use_container_width=True):
        enviar(b"p")
with col_d:
    if st.button("➡️ D — Dir", use_container_width=True):
        enviar(b"d")

# Trás
col_esp3, col_s, col_esp4 = st.columns([1, 1, 1])
with col_s:
    if st.button("⬇️ S — Trás", use_container_width=True):
        enviar(b"s")

# ── Status de conexão ────────────────────────────────────────
st.divider()
if st.session_state.cliente:
    st.success(f"✅ Conectado em {ip}:{porta}")
else:
    st.warning("⚠️ Desconectado")