import pygame
from lutadores import Lutador

pygame.init()

# Criando a janela para o game, sendo a primeira variável para largura e a segunda a altura
tela_largura = 1000
tela_altura = 600

tela_jogo = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption("Strife")

# Carregando imagem de fundo
fundo = pygame.image.load("assets/imagens/fundo.jpg").convert_alpha()

# Função para o plano de fundo
def plano_de_fundo():
    escala_img = pygame.transform.scale(fundo, (tela_largura, tela_altura))
    tela_jogo.blit(escala_img, (0, 0))


# Loop do jogo
run = True
while run:

    # Adicionar fundo em loop
    plano_de_fundo()


    # Modo para ser possível a parada do loop e sair do jogo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            run = False

    # Atualizando a exibição
    pygame.display.update()

# Saída do game após o loop
pygame.quit()