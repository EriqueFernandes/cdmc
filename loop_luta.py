import pygame
from pygame import mixer
from fighter import Fighter
from auxiliares import *
from components import Text

def luta(path_mapa) -> False:
  """Nessa função está sendo executada todo desenho do jogo na tela em que foi criada pelo pygame. Para isso foram utilizadas as 
  variáveis com plano de fundo, detalhes e personagens.

  :return: Retorna Falso paraa que consiga ser iniciada a tela da batalha após clicar em Start no menu
  :rtype: False
  """  
  cores = importa_json()[0]
  pygame.init()
  mixer.init()
  # Tamanho da janela 
  SCREEN_WIDTH = 1000
  SCREEN_HEIGHT = 600
  
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  pygame.display.set_caption("Death Strife")

  # Carregando imagem de fundo
  bg_image = pygame.image.load(path_mapa).convert_alpha()

  # Função para o plano de fundo
  def plano_de_fundo():
    """ É criado plano de fundo dentro da tela e desenhada durante todo o tempo
    """  
    escala_img = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(escala_img, (0, 0))

  #frame
  clock = pygame.time.Clock()
  FPS = 60

  #cores
  RED = (255, 0, 0)
  GRAY = (55, 55, 55)
  WHITE = (255, 255, 255)

  #Variáveis do jogo 
  intro_count = 3
  last_count_update = pygame.time.get_ticks()
  score = [0, 0]  # pontuação dos jogadores
  round_over = False
  ROUND_OVER_COOLDOWN = 2000

  #Variavéis dos personagens ( sprites )
  WARRIOR_SIZE = 162
  WARRIOR_SCALE = 4
  WARRIOR_OFFSET = [72, 35]
  WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
  WIZARD_SIZE = 250
  WIZARD_SCALE = 4
  WIZARD_OFFSET = [112, 100]
  WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

  # Carregando sons
  pygame.mixer.music.load("assets/som/music_fundo.mp3")
  pygame.mixer.music.set_volume(0.3)
  pygame.mixer.music.play(-1, 0.0, 5000)
  sword_atk1 = pygame.mixer.Sound("assets/som/guerreiro_ataque1.mp3")
  sword_atk1.set_volume(0.75)
  # sword_atk2 = pygame.mixer.Sound("assets/som/guerreiro_ataque2.mp3")
  # sword_atk2.set_volume(0.75)
  magic_atk1 = pygame.mixer.Sound("assets/som/mago_ataque1.mp3")
  magic_atk1.set_volume(0.75)
  # magic_atk2 = pygame.mixer.Sound("assets/som/mago_ataque2.mp3")
  # magic_atk2.set_volume(0.5)

  # Sprite dos Jogadores
  warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
  wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

  # Mensagem de vitoria
  victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

  # Número de quadros de cada ação das sprites
  WARRIOR_ANIMATION_STEPS = [6, 7, 1, 4, 4, 3, 6]
  WIZARD_ANIMATION_STEPS = [6, 8, 1, 8, 8, 3, 7]

  # Fonte
  count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
  score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

  # Função que desenha o texto 
  def draw_text(text, font, text_col, x, y):
    """função para acrescentar texto na tela no jogo

    :param text: Texto para ser desenhado na tela
    :type text: String
    :param font: fonte para o texto
    :type font: pygame.font.Font
    :param text_col: cor para o texto
    :type text_col: tuple
    :param x: valor de posição do eixo x
    :type x: float
    :param y: valor de posição do eixo y
    :type y: float
    """    
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

  # Função que mostra a barra de vida dos jogadores
  def draw_health_bar(health, x, y):
    """Função para exibição da barra de vida dos personagens

    :param health: valor da quantidade de vida
    :type health: float
    :param x: valor de posição do eixo x
    :type x: float
    :param y: valor de posição do eixo y
    :type y: float
    """    
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, GRAY, (x, y, 400, 30))
    pygame.draw.rect(screen, RED, (x, y, 400 * ratio, 30))


  # As duas instancias dos jogadores
  fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_atk1)
  fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_atk1)

  #icon
  pygame_icon = pygame.image.load('./static/assets/logo.png')
  pygame.display.set_icon(pygame_icon)
  # Loop luta   
  run = True
  while run:
    screen.fill((123,123,123))
    clock.tick(FPS)

    # Adicionar fundo em loop
    plano_de_fundo()

    # Aqui mostra as estatisticas dos jogadores
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("GUERREIRO: " + str(score[0]), score_font, WHITE, 20, 60)
    draw_text("MAGO: " + str(score[1]), score_font, WHITE, 580, 60)
    draw_text("VS", count_font, WHITE, 460,0)

    #update da contagem regressiva
    if intro_count <= 0:

      # Move os lutadores
      fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
      fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
      # Conta o tempo do display 
      draw_text(str(intro_count), count_font, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
      #update conometro 
      if (pygame.time.get_ticks() - last_count_update) >= 1000:
        intro_count -= 1
        last_count_update = pygame.time.get_ticks()

    #update lutadores
    fighter_1.update()
    fighter_2.update()

    #desenha os lutadores
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # Checa se o jogador morreu 
    if round_over == False:
      if fighter_1.alive == False:
        score[1] += 1
        round_over = True
        round_over_time = pygame.time.get_ticks()
      elif fighter_2.alive == False:
        score[0] += 1
        round_over = True
        round_over_time = pygame.time.get_ticks()
    else:
      # Mostra a imagem de vitória 
      screen.blit(victory_img, (260, 180))
      if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
        round_over = False
        intro_count = 3
        fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_atk1)
        fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_atk1)

    # eventos 
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False


    pygame.display.update()
  return False