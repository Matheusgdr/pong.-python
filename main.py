# Importa a biblioteca pygame, que possui ferramentas para criar jogos
import pygame
import random

# Inicializa todos os módulos principais do pygame
pygame.init()

# Cria a janela do jogo com largura 800 e altura 400
tela = pygame.display.set_mode((800, 400))

# Define o título da janela
pygame.display.set_caption("Pong")

# Controla o FPS do jogo
clock = pygame.time.Clock()

# Variável de controle do loop principal
rodando = True

# Classe das barras do Pong
class Barra:

    # Método construtor da barra
    def __init__(self, x, y, largura, altura, velocidade, direcao):

        # Atributos da barra
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.velocidade = velocidade
        self.direcao = direcao

    # Método responsável por desenhar a barra na tela
    def desenhar(self, tela):

        pygame.draw.rect(
            tela,
            (255, 255, 255),
            (self.x, self.y, self.largura, self.altura),
            2
        )

    # Método de movimento automático (usado na barra direita apenas):
    def mover_automaticamente(self):

        self.y += self.velocidade * self.direcao

        if self.y <= 25:
            self.direcao = 1

        if self.y + self.altura >= 375:
            self.direcao = -1

# Classe da bola:
class Bola:

    # Método construtor da bola:
    def __init__(self, x, y, raio, velocidade, direcao_x, direcao_y):
        # Atibutos da bola
        self.x = x
        self.y = y
        self.raio = raio
        self.velocidade = velocidade
        self.direcao_x = direcao_x
        self.direcao_y = direcao_y

    def reiniciar(self):

    # Volta a bola para o centro da tela
        self.x = 400
        self.y = 200

    # Sorteia se a bola vai começar indo para a esquerda ou direita
        self.direcao_x = random.choice([-1, 1])

    # Sorteia se a bola vai começar subindo ou descendo
        self.direcao_y = random.choice([-1, 1])


    # Método responsável por movimentar automaticamente a bola
    def mover(self):

        # Atualiza a posição horizontal da bola.
        # direcao_x = 1  → direita
        # direcao_x = -1 → esquerda
        self.x += self.velocidade * self.direcao_x

        # Atualiza a posição vertical da bola.
        # direcao_y = 1  → desce
        # direcao_y = -1 → sobe
        self.y += self.velocidade * self.direcao_y

        # ==============================
        # EXTREMIDADES DA BOLA
        # ==============================
        # Como self.x e self.y representam o CENTRO da bola,
        # precisamos calcular onde estão suas extremidades.

        # Coordenada do topo da bola
        topo_bola = self.y - self.raio

        # Coordenada da base da bola
        base_bola = self.y + self.raio

        # Coordenada da extremidade esquerda da bola
        esquerda_bola = self.x - self.raio

        # Coordenada da extremidade direita da bola
        direita_bola = self.x + self.raio

        # ==============================
        # COLISÕES VERTICAIS
        # ==============================

        # Se o topo da bola atingir o topo do campo (y = 25),
        # a bola passa a descer.
        if topo_bola <= 25:
            self.direcao_y = 1

        # Se a base da bola atingir o fundo do campo (y = 375),
        # a bola passa a subir.
        if base_bola >= 375:
            self.direcao_y = -1

        # ==============================
        # COLISÕES HORIZONTAIS
        # ==============================

        # Se a bola sair pela parede esquerda, o jogador da direita marca ponto
        if esquerda_bola <= 25:
            return "ponto_direita"

        # Se a bola sair pela parede direita, o jogador da esquerda marca ponto
        if direita_bola >= 775:
            return "ponto_esquerda"

    # Método responsável por desenhar a bola na tela
    def desenhar(self, tela):

        pygame.draw.circle(
        tela,
        (255, 255, 255),
        (self.x, self.y),
        self.raio
        )

# Variáveis de placar
pontos_esquerda = 0
pontos_direita = 0
    
# Fonte para placar:
fonte = pygame.font.SysFont(None, 40)

# Cria os objetos barra e bola
barra_esquerda = Barra(50, 150, 25, 80, 5, 1)
barra_direita = Barra(725, 150, 25, 80, 3, 1)
bola = Bola(400, 200, 10, 5, 1, -1)

# Loop principal do jogo
while rodando:

    # Define o máximo de FPS do jogo
    clock.tick(60)

    # Percorre os eventos do jogo
    for evento in pygame.event.get():

        # Verifica se o usuário fechou a janela
        if evento.type == pygame.QUIT:
            rodando = False

    # Verifica teclas pressionadas
    teclas_pressionadas = pygame.key.get_pressed()

    # Movimenta a barra esquerda para cima e limita o movimento do topo:
    if teclas_pressionadas[pygame.K_UP] and barra_esquerda.y > 25:
        barra_esquerda.y -= barra_esquerda.velocidade

    # Movimenta a barra esquerda para baixo e limita o movimento da base:
    if teclas_pressionadas[pygame.K_DOWN] and barra_esquerda.y + barra_esquerda.altura < 375:
        barra_esquerda.y += barra_esquerda.velocidade

    # Movimenta a barra direita automaticamente:
    barra_direita.mover_automaticamente()

    # Movimenta a bola e verifica se houve ponto
    resultado = bola.mover()

    if resultado == "ponto_direita":
        pontos_direita += 1
        bola.reiniciar()

    if resultado == "ponto_esquerda":
        pontos_esquerda += 1
        bola.reiniciar()

    # Extremidades da bola
    esquerda_bola = bola.x - bola.raio
    direita_bola = bola.x + bola.raio
    topo_bola = bola.y - bola.raio
    base_bola = bola.y + bola.raio

    # Variáveis da barra esquerda
    direita_barra_esquerda = barra_esquerda.x + barra_esquerda.largura
    topo_barra_esquerda = barra_esquerda.y
    base_barra_esquerda = barra_esquerda.y + barra_esquerda.altura
    
    # Colisão com barra esquerda 
    if (
    bola.direcao_x == -1
    and esquerda_bola <= direita_barra_esquerda
    and direita_bola >= barra_esquerda.x
    and base_bola >= topo_barra_esquerda
    and topo_bola <= base_barra_esquerda
):
        bola.direcao_x = 1

    # Variáveis da barra direita: 
    esquerda_barra_direita = barra_direita.x
    topo_barra_direita = barra_direita.y
    base_barra_direita = barra_direita.y + barra_direita.altura

    # Colisão barra direita
    if (
    bola.direcao_x == 1
    and direita_bola >= esquerda_barra_direita
    and esquerda_bola <= barra_direita.x + barra_direita.largura
    and base_bola >= topo_barra_direita
    and topo_bola <= base_barra_direita
):
        bola.direcao_x = -1

    # Preenche a tela com preto
    tela.fill((0, 0, 0))

    # Desenha o campo do jogo
    pygame.draw.rect(
        tela,
        (255, 255, 255),
        (25, 25, 750, 350),
        2
    )  

    # Desenha as barras
    barra_esquerda.desenhar(tela)
    barra_direita.desenhar(tela)

    # Desenha a bola
    bola.desenhar(tela)

    # Cria uma imagem de texto com a pontuação atual
    texto_esquerda = fonte.render(str(pontos_esquerda), True, (255, 255, 255))
    texto_direita = fonte.render(str(pontos_direita), True, (255, 255, 255))

    # Desenha as imagens do placar na tela
    tela.blit(texto_esquerda, (300, 40))
    tela.blit(texto_direita, (480, 40))

    # Atualiza a tela
    pygame.display.update()

# Finaliza corretamente o pygame
pygame.quit()