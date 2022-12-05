import json

def converte_cor(cor):
    """recebe um texto que represente uma cor em padrao hexadecimal e devolve o RGB correspondente

    :param cor: string do hexadecimal de uma cor
    :type cor: str
    :return: retorna uma tupla com o RGB da cor
    :rtype: tuple
    """    
    if isinstance(cor,tuple):
        return cor
    color = cor.lstrip('#')
    color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    
    return color

def importa_json() -> dict:
    """A funcao abre o arquivo json e retorna dois dicionarios com dados relacionados com o jogo. 

    :return: O primeiro sao as cores utilizadas e o segundo sao os que impactam no jogo
    :rtype: dict
    """    
    cores = {}
    data = {}
    with open("./config/config.json", "r", encoding="utf-8") as f:
        d = json.load(f)

        for k, v in d.items():
            if k == "colors":
                for cor, hexa in v.items():
                    cores[cor] = converte_cor(hexa)
            else:
                data[k] = v

    return cores, data

def break_text(texto, y, fonte, largura_maxima, div_linha):
    """A funcao recebe um texto e devolve uma lista com linhas para serem exibidas na tela

    :param texto: O texto que deve ser exibido
    :type texto: str
    :param y: a posicao inicial y em que o texto deve aparecer
    :type y: int
    :param fonte: fonte pygame para ser renderizada
    :type fonte: pygame.Font
    :param largura_maxima: a largura do container que ira conter o texto
    :type largura_maxima: int
    :param div_linha: a distancia entre as linhas do texto
    :type div_linha: int
    :return: retorna uma lista com o texto recebido como argumento quebrado em linhas que caibam na largura especificada
    :rtype: list
    """    
    palavras = texto.split()
    linhas = []
    linha = []
    while len(palavras) > 0:
        linha.append(palavras.pop(0))
        plus = ""
        if len(palavras) != 0:
            plus = palavras[0]
        wi, he = fonte.size(" ".join(linha) + plus)
        if wi > largura_maxima or len(palavras) == 0 and len(linha) != 0 or linha[0].startswith("\\"):
            if linha[0].startswith("\\"): linha[0] = linha[0][1:]
            y_h = y + (he + div_linha) * len(linhas) 
            linhas.append((linha, y_h))
            linha = []

    return linhas