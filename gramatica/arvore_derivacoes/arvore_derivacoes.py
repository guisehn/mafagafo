# -*- coding: utf-8 -*-
import re
from no_arvore_derivacoes import *
from gerador_derivacoes import *
from gramatica.util import *
from constants import *

class ArvoreDerivacoes:
    def __init__(self, gramatica):
        self.gramatica = gramatica
        self.gerador_derivacoes = GeradorDerivacoes(gramatica)
        self.limpar_arvore()

    def limpar_arvore(self):
        """Volta a árvore para seu estado inicial"""
        self.raiz = NoArvoreDerivacoes(self.gramatica.simbolo_inicial)
        self.folhas = [self.raiz]

    def montar_sem_recursao(self):
        """Monta árvore de derivações sem recursão de símbolos NT"""
        self.limpar_arvore()
        while self.gerar_novo_nivel(True): pass
        return self

    def gerar_novo_nivel(self, impedir_recursao):
        """
        Gera novo nível de derivações para a árvore.
        Defina o parâmetro impedir_recursao como True se você não quiser gerar
        novos níveis para nós que possuem sentenças com símbolos não-terminais que
        já foram derivados para chegar até ele.
        """
        progresso = False
        nova_lista_folhas = []

        for no in self.folhas:
            if not sentenca_contem_nt(no.sentenca):
                nova_lista_folhas.append(no)
                continue

            if impedir_recursao and no.contem_recursao():
                nova_lista_folhas.append(no)
                continue

            progresso = True
            derivacoes = self.gerador_derivacoes.gerar_derivacoes(no.sentenca)
            for derivacao in derivacoes:
                nova_folha = NoArvoreDerivacoes(derivacao, no)
                no.nos.append(nova_folha)
                nova_lista_folhas.append(nova_folha)

        if progresso:
            self.folhas = nova_lista_folhas

        return progresso

    def pode_gerar_sentenca_finita(self):
        """
        Verifica se a gramática pode gerar ao menos uma sentença finita.
        A árvore já deve estar montada para chamar este método.
        """
        return any(not sentenca_contem_nt(no.sentenca) for no in self.folhas)

    def buscar_nos_de_sentencas_finais(self):
        """Busca nós das sentenças finais na árvore"""
        return [no for no in self.folhas if sentenca_eh_final(no.sentenca)]

    def buscar_sentencas_finais(self):
        """Busca todas as sentenças finais geradas na árvore"""
        return [no.sentenca for no in self.buscar_nos_de_sentencas_finais()]

    def buscar_sentencas_minimas(self):
        """Busca sentenças mínimas da gramática"""
        sentencas_minimas = []
        sentencas_finais = self.buscar_sentencas_finais()

        if sentencas_finais:
            tamanho_minimo = len(min(sentencas_finais, key = lambda s: len(s)))
            sentencas_minimas = [s for s in sentencas_finais if len(s) == tamanho_minimo]
        
        return sentencas_minimas