import pygame
from pygame.locals import *

pygame.init()

largura = 1200
altura = 700
relogio = pygame.time.Clock()

tela = pygame.display.set_mode((largura, altura))
fundo = pygame.transform.scale(pygame.image.load('fundo.jpg'), (largura, altura))

def cenario():
    tela.blit(fundo, (0, 0))

class Personagem():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x,y,100, 200))
        self.alt_pulo = 0
        self.pulo = False

    def movimentos(self):
        velocidade = 10
        gravidade = 2
        x = 0
        y = 0
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            x = -velocidade
        if key[pygame.K_RIGHT]:
            x = velocidade
        if key[pygame.K_UP] and self.pulo == False:
            self.alt_pulo = -30
            self.pulo = True

        self.alt_pulo += gravidade
        y += self.alt_pulo

        if self.rect.left + x < 0:
            x = -self.rect.left
        if self.rect.right + x > largura:
            x = largura - self.rect.right
        if self.rect.bottom + y > altura -50:
            self.alt_pulo = 0
            self.pulo = False
            y = altura -50 - self.rect.bottom

        self.rect.x += x
        self.rect.y += y

    def img_jogador(self, tela):
        pygame.draw.rect(tela, (50, 170, 50), self.rect)

jogador_2 = Personagem(200, 450)

while True:

    relogio.tick(30)
    cenario()
    jogador_2.movimentos()
    jogador_2.img_jogador(tela)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    
    pygame.display.flip()
