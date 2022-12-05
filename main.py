import pygame
from pygame import mixer
from loop_luta import luta
from auxiliares import *

class Box():
    def __init__(self, largura, altura):
        """ Construtor da classe
        :param largura: largura para tela
        :type largura: float
        :param altura: altura para tela
        :type altura: float
        """        
        self.largura = largura
        self.altura = altura 

    def draw(self,surface, coordenada, background_color, centralizado = False, box_shadow = None, borda = None):
        """ Função para desenhar objetos

        :param surface: superfície para desenho
        :type surface: pygame.Surface
        :param coordenada: lista de coordenada envolvendo eixo x e y
        :type coordenada: list
        :param background_color: cor do background
        :type background_color: tuple
        :param centralizado: caso para centralização de objeto
        :type centralizado: bool
        :param box_shadow: sombra para caixa
        :type box_shadow: list
        :param borda: borda para caixa
        :type borda: list
        """        
        self.x = coordenada[0] 
        self.y = coordenada[1]
        self.background_color = background_color
        tmp = 0

        if centralizado:
            self.x -= self.largura / 2
            self.y -= self.altura / 2

        ret_inside = [self.x, self.y, self.largura, self.altura]

        ret_bordas = []

        if not borda is None:
            espessura = borda[0]
            x_start, x_end = self.x - espessura, self.x + self.largura
            y_start, y_end = self.y - espessura, self.y + self.altura

            ret_bordas = [[x_start, y_start, espessura, self.altura + 2 * espessura],
                            [self.x, y_start, self.largura, espessura],
                            [self.x, y_end, self.largura, espessura],
                            [x_end, y_start, espessura, self.altura + 2 * espessura]]

            tmp = espessura

        if not box_shadow is None:
            x_bs, y_bs = box_shadow[0], box_shadow[1]
            ret_box_shadow = [self.x + x_bs, self.y + y_bs, self.largura + tmp, self.altura + tmp]

            pygame.draw.rect(surface, box_shadow[2], ret_box_shadow)
        
        pygame.draw.rect(surface, self.background_color, ret_inside)

        for ret in ret_bordas:
            pygame.draw.rect(surface, borda[1], ret)

class Text():
    def __init__(self, texto, font_family, font_size, color, action = None):
        """ Construtor da classe

        :param texto: texto para uso
        :type texto: String
        :param font_family: font para texto
        :type font_family: String
        :param font_size: tamanho da letra
        :type font_size: float
        :param color: cor para texto
        :type color: tuple
        :param action: ação de objeto
        :type action: String
        """        
        print(type(font_family))
        self.font = pygame.font.Font(font_family , font_size)
        self.conteudo_texto = texto
        self.texto_renderizado = self.font.render(texto, False, color)
        self.rect = self.texto_renderizado.get_rect()
        self.action = action
        self.color = color
        self.std_input = False
        if action == "change_key":
            self.input_on = False

    def draw(self, surface, coordenada, text_shadow=None, background_color=None, centralizado=False, box_shadow=None, borda=None, padding = 5, max_width = None):
        """ Função para desenhar texto

        :param surface: superfície para desenho
        :type surface: pygame.Surface
        :param coordenada: lista de coordenada envolvendo eixo x e y
        :type coordenada: list
        :param text_shadow: sombra para texto
        :type text_shadow: list
        :param background_color: cor para fundo
        :type background_color: tuple
        :param centralizado: caso para centralização de objeto
        :type centralizado: bool
        :param box_shadow: sombra para caixa
        :type box_shadow: list
        :param borda: borda para caixa de texto
        :type borda: list
        :param padding: preenchimento da caixa
        :type padding: int
        :param max_width: tamanho máximo
        :type max_width: float
        """        
        self.surface = surface
        self.largura, self.altura = self.rect[2], self.rect[3]
        self.text_shadow = text_shadow
        self.background_color = background_color
        self.centralizado = centralizado
        self.box_shadow = box_shadow
        self.borda = borda
        self.padding = padding
        self.max_width = max_width
        if background_color is None:
            x, y = coordenada
            
            self.largura, self.altura = self.rect[2], self.rect[3]
            
            if centralizado:
                x = coordenada[0] - self.rect.width / 2
                y = coordenada[1] - self.rect.height / 2

            if not text_shadow is None:
                if not max_width is None:
                    linhas = break_text(self.conteudo_texto, y, self.font, max_width, div_linha = 15)
                    for row in linhas:
                        texto = self.font.render(" ".join(row[0]), False, text_shadow[2])
                        surface.blit(texto , (x + text_shadow[0], row[1] + text_shadow[1]))
                        texto = self.font.render(" ".join(row[0]), False, self.color)
                        surface.blit(texto , (x , row[1] ))
                    return

                texto = self.font.render(self.conteudo_texto, False, text_shadow[2])
                surface.blit(texto, (x + text_shadow[0], y + text_shadow[1]))

            if not max_width is None:
                texto = break_text(self.conteudo_texto, y, self.font, max_width, div_linha = 15)
                for row in texto:
                    texto_render = self.font.render(" ".join(row[0]), False, self.color)
                    surface.blit(texto_render, (x, row[1]))
                return

            surface.blit(self.texto_renderizado, (x, y))

            self.x, self.y = x, y
            return 

        box_bg = Box(self.rect.width + 2 * padding, self.rect.height + 2 * padding)
        box_bg.draw(surface=surface, coordenada=coordenada,background_color=background_color, centralizado=centralizado, box_shadow=box_shadow, borda=borda)
        
        x = box_bg.x + (box_bg.largura - self.rect.width) / 2 
        y = box_bg.y + (box_bg.altura - self.rect.height) / 2 

        if not text_shadow is None:
            texto = self.font.render(self.conteudo_texto, False, text_shadow[2])
            surface.blit(texto, (x + text_shadow[0], y + text_shadow[1]))
        
        
        surface.blit(self.texto_renderizado, (x, y))
        self.largura, self.altura = box_bg.largura, box_bg.altura
        self.x, self.y = box_bg.x, box_bg.y

    def click(self) -> int:
        """ Função para clique em caixas

        :return: valor da caixa selecionada
        :rtype: int
        """        
        # mudar tela dependendo da action
        if self.action == "menu":
            return 1
        elif self.action == "jogar":
            return 2
        elif self.action == "config":
            return 3
        elif self.action == "sair":
            return 4
        elif self.action == "creditos":
            return 5
        
class Game():
    def __init__(self):
        #starta pygame modulo
        pygame.init()

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

        # setando lista elementos na tela
        self.lista_botoes = []
        self.componentes = {}

        # cor de fundo
        self.background_color = converte_cor("#535c68")
        
        #ajusta variavel relogio
        self.relogio = pygame.time.Clock()
        
        #coloca tela
        self.tela = pygame.display.set_mode((self.width, self.height))
        
        #ajusta mouse
        # pygame.mouse.set_visible(False)
        # self.cursor_mouse = pygame.image.load("img/icon_mouse.png").convert()
        
        #ajusta fonte
        self.font_family = "assets/fonts/PressStart2p.ttf"
        
        #coloca o titulo
        pygame.display.set_caption("Death Strife")
        
        #abre tela
        pygame.display.update()
        
        #roda loop do jogo
        self.loop()
        
    def draw_menu(self):

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

    def draw_cenario(self):
        # PS: se as bordas nao alterarem a largura e altura nao é preciso de dois bg_life
        bg_life= Box(self.width * .35, self.height * .05)
        x = (self.width * .05, self.width * .95 - bg_life.largura )
        y = self.height * .05
        bg_life.draw(coordenada = (x[0],y), surface = self.tela, background_color = self.colors["violeta"], borda = [5, self.colors["azul_depth"]])
        bg_life.draw(coordenada = (x[1],y), surface = self.tela, background_color = self.colors["violeta"], borda = [5, self.colors["azul_depth"]])
        life_p1 = Box(self.width * .2, self.height * .05)
        life_p2 = Box(self.width * .3, self.height * .05)
        life_p1.draw(coordenada = (x[0], y), surface = self.tela, background_color = self.colors["pink_neon"])
        life_p2.draw(coordenada = (x[1], y), surface = self.tela, background_color = self.colors["pink_neon"])

        self.componentes["vida_p1"] = life_p1
        self.componentes["vida_p2"] = life_p2

        texto_vs = Text("VS", self.font_family, font_size= 40, color = self.colors["preto_neon"])
        self.componentes["texto_vs"] = texto_vs
        texto_vs.draw(self.tela, (self.width /2, self.height * .1), centralizado= True, text_shadow=[3,3, self.colors["coral"]] )

    def draw_config(self):
        lista_botoes = []
        
        bg_config = Box(self.width * .4, self.height * .8)
        bg_config.draw(self.tela, (self.width/ 2, self.height / 2), self.colors["preto_neon"], True, borda = [5,self.colors["branco_neon"]])
        #btn_controles = Text("Controles", self.font_family, 35, self.colors["branco_comum"], action = "controles")
        #btn_som = Text("Som", self.font_family, 35, self.colors["branco_comum"], action = "som")
        btn_creditos = Text("Creditos", self.font_family, 35, self.colors["branco_comum"], action = "creditos")
        btn_voltar = Text("Voltar", self.font_family, 35, self.colors["branco_comum"], action = "menu")
        
        #lista_botoes.append(btn_controles)
        #lista_botoes.append(btn_som)
        lista_botoes.append(btn_creditos)
        lista_botoes.append(btn_voltar)

        self.lista_botoes = lista_botoes
        for _ in lista_botoes:
            index = lista_botoes.index(_)
            altura = 0
            margin = 50
            if index > 0:
                altura = lista_botoes[index - 1].altura
            _.draw(self.tela, (self.width / 2, self.height  * 0.2 + index * (altura+ margin)), [2, 2, self.colors["rosa_choque"]], self.colors["cinza_claro"], True, padding = 10 , borda=[1, self.colors["rosa_choque"]])

    def draw_creditos(self):
        bg = Box(self.width * .6, self.height * .6)
        bg.draw(self.tela, (self.width / 2, self.height / 2), self.colors["preto_neon"], True, borda=[3,self.colors["cinza_claro"]])
        agradecimentos = Text(self.data["creditos"]["texto"], self.font_family, 20, self.colors["branco_comum"])
        agradecimentos.draw(self.tela, (bg.x + bg.largura * .1, bg.y + bg.altura * .1), max_width = bg.largura * .8, text_shadow=[1,1,self.colors["jade_dust"]])       
        btn_close = Text("X", self.font_family, 30, self.colors["rosa_choque"], action = "config")
        btn_close.draw(self.tela, (bg.x + bg.largura - btn_close.rect[2] * 1.5, bg.y + btn_close.rect[3]/2), [3,3, self.colors["branco_neon"]])
        self.lista_botoes.append(btn_close)


    def loop(self):
        while self.run:
            self.relogio.tick(60)
            self.tela.fill(self.background_color )
            x, y = pygame.mouse.get_pos()


            if self.n_tela == 1:
                self.draw_menu()

            elif self.n_tela == 2:
                #self.draw_cenario()
                x = luta()
                if x is False:
                    self.run = False
            elif self.n_tela == 3:
                self.draw_config()
            elif self.n_tela == 4:
                self.run = False
            elif self.n_tela == 5:
                self.draw_creditos()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.run = False
                    
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    for btn in self.lista_botoes:
                        if not btn.x + btn.largura >= x >= btn.x or not btn.y + btn.altura >= y >= btn.y: continue
                        self.lista_botoes = []
                        self.n_tela = btn.click()

            pygame.display.flip()

        #rodado caso o jogo encerre
        pygame.display.quit()
        
g = Game()
