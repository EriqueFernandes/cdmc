import pygame
from loop_luta import luta
from auxiliares import *
from components import *
#starta pygame modulo
pygame.init()

class Game():
    def __init__(self):
        """Construtor para iniciar as variáveis necessárias para o jogo
        """        
        #importando dados base
        importando = importa_json()
        self.colors = importando[0]
        self.data = importando[1]

        #ajustando variáveis iniciais
        self.run = True
        self.width = self.data["screen"]["width"]
        self.height = self.data["screen"]["height"]
        self.desenhado = False
        self.n_tela = 1
        self.n_mapa = 0

        # setando lista elementos na tela
        self.lista_botoes = []
        self.componentes = {}

        # cor de fundo
        self.background_color = converte_cor("#535c68")
        
        #ajusta variavel relogio
        self.relogio = pygame.time.Clock()
        
        #coloca tela
        self.tela = pygame.display.set_mode((self.width, self.height))
        
        #ajusta fonte
        self.font_family = "assets/fonts/PressStart2p.ttf"
        
        #coloca icone
        pygame_icon = pygame.image.load('./static/assets/logo.png')
        pygame.display.set_icon(pygame_icon)

        #coloca o titulo
        pygame.display.set_caption("Death Strife")
        
        #abre tela
        pygame.display.update()
        
        #roda loop do jogo
        self.loop()
        
    def draw_menu(self):
        """funcao utilizada para desenhar o menu principal com seus componentes e botoes
        """        
        # titulo
        hello = Text("Death strife", self.font_family, 70, self.colors["pink_neon"])
        hello.draw(self.tela, (self.width / 2,  self.height * .2), [3,3,self.colors["preto_neon"]], centralizado = True)

        # botoes menu principal
        button_start = Text("START", self.font_family, 25, self.colors["pink_neon"], action = "jogar")
        button_exit = Text("SAIR", self.font_family, 25, self.colors["pink_neon"], action = "sair")
        button_config = Text("CONFIG", self.font_family, 25, self.colors["pink_neon"], action = "config")
        
        # Nas configurações é interessante mudar as cores pra dar ou ent tirar o som
        self.lista_botoes.append(button_start)
        self.lista_botoes.append(button_config)
        self.lista_botoes.append(button_exit)
        
        # desenhando 
        for _ in self.lista_botoes:
            margin = 0
            index_atual = self.lista_botoes.index(_)
            altura = 0

            if index_atual > 0:
                altura = self.lista_botoes[index_atual - 1].altura
                margin = 50

            y = self.height * .2 + hello.rect[3] + 100+  (altura + margin )* index_atual 
            x = self.width / 2
            _.draw(self.tela, (x,y), [2,2,self.colors["branco_neon"]], self.colors["preto_neon"], True, [3,3,self.colors["pink_neon"]], [3,self.colors["branco_neon"]], 20)

    def draw_choose_cenario(self):
        """exibe um mini menu ppara o usuario escolher qual fase quer jogar
        """        
        cenarios = self.data["cenarios"]
        he = None
        for i in range(len(cenarios)):
            btn = Text(f'cenario {i}', self.font_family, 25, self.colors["kirby"], action="choose_cenario")
            btn.draw(self.tela, (self.width * .1 + i * (btn.rect[2] + 40),self.height / 2 + 3 * btn.rect[3]), [3,3,self.colors["branco_neon"]], self.colors["preto_neon"], False, [3,3,self.colors["azul_depth"]], [3, self.colors["branco_neon"]])
            img = pygame.image.load(cenarios[i]).convert()
            ret_img = img.get_rect()
            escala =  ret_img[2] / btn.largura
            if i == 0:
                he = ret_img[3] / escala
            img = pygame.transform.scale(img, (btn.largura, he))
            self.tela.blit(img, (btn.x, btn.y - img.get_rect()[3] - 50))
            self.lista_botoes.append(btn)

    def draw_config(self):
        """funcao desenha o menu de configuracoes e seus botoes
        """        
        lista_botoes = []
        
        bg_config = Box(self.width * .4, self.height * .8)
        bg_config.draw(self.tela, (self.width/ 2, self.height / 2), self.colors["preto_neon"], True, borda = [5,self.colors["branco_neon"]])
        btn_controles = Text("Controles", self.font_family, 35, self.colors["pink_neon"], action = "controles")
        btn_creditos = Text("Creditos", self.font_family, 35, self.colors["pink_neon"], action = "creditos")
        btn_voltar = Text("Voltar", self.font_family, 35, self.colors["pink_neon"], action = "menu")
        
        lista_botoes.append(btn_controles)
        lista_botoes.append(btn_creditos)
        lista_botoes.append(btn_voltar)

        self.lista_botoes = lista_botoes
        for _ in lista_botoes:
            index = lista_botoes.index(_)
            altura = 0
            margin = 50
            if index > 0:
                altura = lista_botoes[index - 1].altura
            _.draw(self.tela, (self.width / 2, self.height  * 0.2 + index * (altura+ margin)), [2, 2, self.colors["preto_neon"]], self.colors["branco_neon"], True, padding = 10, box_shadow= [ 5,5,self.colors["cinza_claro"]])

    def draw_controles(self):
        """esta funcao constroi o menu de exibicao para mostrar as teclas utilizadas no jogo
        """        
        bg = Box(self.width * .8, self.height * .6)
        bg.draw(self.tela, (self.width / 2, self.height / 2), self.colors["preto_neon"], True, borda=[3,self.colors["cinza_claro"]])
        container = Box(bg.largura * .4, bg.altura * .9)
        x = [bg.x + bg.largura * .075, bg.x + bg.largura * .925 - container.largura]
        container.draw(self.tela, (x[0], bg.y + bg.altura * .05), self.colors["branco_neon"])
        container.draw(self.tela, (x[1], bg.y + bg.altura * .05), self.colors["branco_neon"])
        btn_close = Text("X", self.font_family, 30, self.colors["pink_neon"], action = "config")
        btn_close.draw(self.tela, (bg.x + bg.largura - btn_close.rect[2] * 1.5, bg.y + btn_close.rect[3]/2), [3,3, self.colors["branco_neon"]])
        self.lista_botoes.append(btn_close)
        p_1 = Text("Player 1", self.font_family, 25, self.colors["pink_neon"])
        p_2 = Text("Player 2", self.font_family, 25, self.colors["pink_neon"])
        p_1.draw(self.tela, (x[0] + (container.largura - p_1.rect.width)/2, container.y + container.altura * .05), [3,3, self.colors["kirby"]])
        p_2.draw(self.tela, (x[1] + (container.largura - p_1.rect.width)/2, container.y + container.altura * .05), [3,3, self.colors["kirby"]])
        # desenhar botoes para mostrar os comando
        
        y_h = p_1.y + p_1.altura + 40

        p_1_teclas = self.data["teclas"]["player_1"]
        p_2_teclas = self.data["teclas"]["player_2"]

        for k, v in p_1_teclas.items():
            movimento = Text(k, self.font_family, 15, self.colors["jade_dust"])
            key = Text(v, self.font_family, 15, self.colors["azul_depth"])
            movimento.draw(self.tela, (x[0] + container.largura * .05, y_h))
            key.draw(self.tela, (x[0] + container.largura/2, y_h),  background_color=self.colors["cinza_claro"])
            y_h += movimento.altura + 20

        y_h = p_1.y + p_1.altura + 40

        for k, v in p_2_teclas.items():
            movimento = Text(k, self.font_family, 15, self.colors["jade_dust"])
            key = Text(v, self.font_family, 15, self.colors["azul_depth"])
            movimento.draw(self.tela, (x[1] + container.largura * .05, y_h))
            key.draw(self.tela, (x[1] + container.largura/2, y_h), background_color=self.colors["cinza_claro"])
            y_h += movimento.altura + 20

    def draw_creditos(self):
        """funcao responsavel por fazer a tela de agradecimento
        """        
        bg = Box(self.width * .75, self.height * .65)
        bg.draw(self.tela, (self.width / 2, self.height / 2), self.colors["preto_neon"], True, borda=[3,self.colors["cinza_claro"]])
        agradecimentos = Text(self.data["creditos"]["texto"], self.font_family, 20, self.colors["pink_neon"])
        agradecimentos.draw(self.tela, (bg.x + bg.largura * .1, bg.y + bg.altura * .1), max_width = bg.largura * .8, text_shadow=[1,1,self.colors["jade_dust"]])       
        btn_close = Text("X", self.font_family, 30, self.colors["pink_neon"], action = "config")
        btn_close.draw(self.tela, (bg.x + bg.largura - btn_close.rect[2] * 1.5, bg.y + btn_close.rect[3]/2), [3,3, self.colors["branco_neon"]])
        self.lista_botoes.append(btn_close)

    def loop(self):
        """Funcao que roda o loopde jogo
        """        
        while self.run:
            self.relogio.tick(60)
            self.tela.fill(self.background_color )
            x, y = pygame.mouse.get_pos()


            if self.n_tela == 1:
                self.draw_menu()

            elif self.n_tela == 2:
                self.draw_choose_cenario()
            elif self.n_tela == 3:
                self.draw_config()
            elif self.n_tela == 4:
                self.run = False
            elif self.n_tela == 5:
                self.draw_creditos()
            elif self.n_tela == 6:
                mapa = self.data["cenarios"][int(self.n_mapa)]
                x = luta(mapa)
                if x is False:
                    self.run = False
            elif self.n_tela == 7:
                self.draw_controles()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.run = False
                    
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    for btn in self.lista_botoes:
                        if not btn.x + btn.largura >= x >= btn.x or not btn.y + btn.altura >= y >= btn.y: continue
                        self.lista_botoes = []
                        self.n_tela = btn.click()
                        if btn.action == "choose_cenario": 
                            self.n_mapa = self.n_tela[1]
                            self.n_tela = self.n_tela[0]
            pygame.display.flip()

        #rodado caso o jogo encerre
        pygame.display.quit()
        
g = Game()
