import pygame
from auxiliares import break_text

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
        self.font = pygame.font.Font(font_family , font_size)
        self.conteudo_texto = texto
        self.texto_renderizado = self.font.render(texto, False, color)
        self.rect = self.texto_renderizado.get_rect()
        self.action = action
        self.color = color

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
        elif self.action == "choose_cenario":
            return 6, self.conteudo_texto[-1]
        elif self.action == "controles":
            return 7