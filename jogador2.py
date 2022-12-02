import pygame
from pygame.locals import *

pygame.init()

largura = 1200
altura = 700
relogio = pygame.time.Clock()

tela = pygame.display.set_mode((largura, altura))
fundo = pygame.transform.scale(pygame.image.load('fundo.jpg'), (largura, altura))

class Personagem():
    def __init__(self, player, x, y):
        self.player = player
        self.rect = pygame.Rect((x,y,100, 200))
        self.alt_pulo = 0
        self.pulo = False
        self.atacando = False
        self.num_ataque = 0

    def movimentacao(self, alvo):
        velocidade = 10
        gravidade = 2
        x = 0
        y = 0
        key = pygame.key.get_pressed()
        
        if self.atacando == False:
            if key[pygame.K_LEFT]:
                x = -velocidade
            if key[pygame.K_RIGHT]:
                x = velocidade
            if key[pygame.K_UP] and self.pulo == False:
                self.alt_pulo = -30
                self.pulo = True
            if key[pygame.K_KP1] or key[pygame.K_KP2]:
                self.ataque(alvo)
                if key[pygame.K_KP1]:
                    self.num_ataque = 1
                if key[pygame.K_KP2]:
                    self.num_ataque = 2

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

    def ataque(self, alvo):
        self.atacando = True
        area_ataque = pygame.Rect(self.rect.centerx, self.rect.y, 2 * self.rect.width, self.rect.height)
        if area_ataque.colliderect(alvo.rect):
            print('ok')
        pygame.draw.rect(tela, (255, 0, 0), area_ataque)

    def img_jogador(self, tela):
        pygame.draw.rect(tela, (50, 170, 50), self.rect)

jogador_1 = Personagem(1, 200, 450)
jogador_2 = Personagem(2, 700, 450)

while True:

    relogio.tick(30)
    tela.blit(fundo, (0, 0))
    jogador_1.img_jogador(tela)
    jogador_2.movimentacao(jogador_1)
    jogador_2.img_jogador(tela)
    

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    
    pygame.display.flip()
