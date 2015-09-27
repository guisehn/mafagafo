import random
import re
from collections import OrderedDict

class GeradorSentencas:
    MAXIMO_ITERACOES = 10000

    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.conjunto_producoes = self.ordenar_conjunto_producoes(self.gramatica.conjunto_producoes)

    def gerar(self, sentenca = 'S'):
        historico = [sentenca]  
        i = 0

        while re.search('[A-Z]', sentenca) and i <= self.MAXIMO_ITERACOES:
            i += 1
            for esquerda, direita in self.conjunto_producoes.iteritems():
                if esquerda in sentenca:
                    indice = random.randint(0, len(direita) - 1)
                    item_direita = direita[indice]
                    sentenca = sentenca.replace(esquerda, item_direita)
                    historico.append(sentenca)
                    break

        return (sentenca, historico)

    def ordenar_conjunto_producoes(self, conjunto_producoes):
        iteritems = conjunto_producoes.iteritems()
        return OrderedDict(sorted(iteritems, key = lambda x: len(x[0])))