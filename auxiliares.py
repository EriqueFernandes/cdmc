import json

def converte_cor(cor):
    if isinstance(cor,tuple):
        return cor
    color = cor.lstrip('#')
    color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    
    return color

def importa_json():
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