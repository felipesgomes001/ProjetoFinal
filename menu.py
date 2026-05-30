import streamlit as st
import socket

if "tela" not in st.session_state:
    st.session_state.tela = "login"

if "cliente" not in st.session_state:
    st.session_state.cliente = None

# TELA DE LOGIN
if st.session_state.tela == "login":
    st.title("Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if usuario == "Steakeholders" and senha == "010203":
            st.balloons()
            import time
            time.sleep(2)
            st.session_state.tela = "controle"
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

# TELA DE CONTROLE
elif st.session_state.tela == "controle":
    st.title("🚗 CONTROLE DO CARRO")

    ip = st.text_input("IP do Rover", value="192.168.7.149")
    porta = st.number_input("Porta", value=5000, step=1)

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

    def enviar(cmd: bytes):
        try:
            if st.session_state.cliente:
                st.session_state.cliente.send(cmd)
            else:
                st.warning("Conecte-se primeiro!")
        except Exception as e:
            st.error(f"Erro ao enviar: {e}")

    st.divider()
    
    # Nível de bateria do carro
    
    if "bateria" not in st.session_state:
        st.session_state.bateria = 67  

    st.subheader("🔋 Bateria")

    if st.session_state.cliente:
        try:
            resposta = st.session_state.cliente.recv(1024).decode()
            if resposta:
                st.session_state.bateria = int(resposta)
        except:
            pass

    bateria = st.session_state.bateria
    st.progress(bateria / 100)
    st.caption(f"{bateria}% de carga")
    st.divider()
    st.subheader("Controle")

    col_esp, col_w, col_esp2 = st.columns([1, 1, 1])
    with col_w:
        if st.button("⬆️ W — Frente", use_container_width=True):
            enviar(b"w")

    col_a, col_p, col_d = st.columns(3)
    with col_a:
        if st.button("⬅️ A — Esquerda", use_container_width=True):
            enviar(b"a")
    with col_p:
        if st.button("⏹️ Parar", use_container_width=True):
            enviar(b"p")
    with col_d:
        if st.button("➡️ D — Direita", use_container_width=True):
            enviar(b"d")

    col_esp3, col_s, col_esp4 = st.columns([1, 1, 1])
    with col_s:
        if st.button("⬇️ S — Trás", use_container_width=True):
            enviar(b"s")

    st.divider()
    if st.session_state.cliente:
        st.success(f"✅ Conectado em {ip}:{porta}")
    else:
        st.warning("⚠️ Desconectado")

    if st.button("Sair"):
        st.session_state.tela = "login"
        st.rerun()