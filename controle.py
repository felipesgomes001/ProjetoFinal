# ============================================================
# controle.py — Cliente de controle do Rover via teclado
# Envia comandos WASD para o servidor do Rover via socket TCP
# ============================================================

import pygame   # Biblioteca para criar a janela e capturar teclas
import socket   # Biblioteca para comunicação via rede (TCP/IP)

# Inicializa todos os módulos do pygame
pygame.init()

# Cria a janela gráfica com tamanho 300x300 pixels
tela = pygame.display.set_mode((300, 300))

# Define a fonte de texto padrão do sistema com tamanho 40
fonte = pygame.font.SysFont(None, 40)

# ── Conexão com o servidor (Rover) ──────────────────────────
# Cria um socket TCP (SOCK_STREAM é o padrão para conexões confiáveis)
cliente = socket.socket()

# Conecta ao servidor do Rover pelo IP e porta definidos
# ⚠️ Altere o IP abaixo para o IP do seu Rover na rede local
cliente.connect(("192.168.7.149", 5000))

# ── Loop principal do programa ───────────────────────────────
while True:

    # Preenche a tela com a cor de fundo (cinza escuro)
    tela.fill((30, 30, 30))

    # Renderiza o texto de instrução em branco
    texto = fonte.render("Use W A S D", True, (255, 255, 255))

    # Desenha o texto na tela na posição (60, 130)
    tela.blit(texto, (60, 130))

    # Atualiza a janela para exibir o que foi desenhado
    pygame.display.update()

    # ── Leitura de eventos (teclado, fechar janela, etc.) ────
    for e in pygame.event.get():

        # Evento de fechar a janela (clicou no X)
        if e.type == pygame.QUIT:
            pygame.quit()  # Encerra o pygame e fecha a janela

        # Evento de tecla pressionada
        if e.type == pygame.KEYDOWN:

            if e.key == pygame.K_w:
                cliente.send(b"w")  # Envia comando: mover para frente

            if e.key == pygame.K_s:
                cliente.send(b"s")  # Envia comando: mover para trás

            if e.key == pygame.K_a:
                cliente.send(b"a")  # Envia comando: virar à esquerda

            if e.key == pygame.K_d:
                cliente.send(b"d")  # Envia comando: virar à direita

        # Evento de tecla solta — para o Rover quando nenhuma tecla está pressionada
        if e.type == pygame.KEYUP:
            cliente.send(b"p")  # Envia comando: parar