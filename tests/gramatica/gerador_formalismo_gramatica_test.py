import unittest
from gramatica import *
from gramatica.gerador_formalismo_gramatica import *
from constants import SIMBOLO_INICIAL as S
from constants import SIMBOLO_SENTENCA_VAZIA as X

class GeradorFormalismoGramaticaTest(unittest.TestCase):
    def test_gerar_formalismo_com_sentenca_vazia(self):
        gramatica = Gramatica(
            [S, 'A', 'B'],
            ['a', 'b', 'c'],
            {
                S: ['AB', 'b'],
                'A': ['aAB', 'Aa', X],
                'B': ['b', 'bB']
            }
        )

        str = 'G = ({S, A, B}, {a, b, c}, P, %s)' % S
        str += '\nP = {\n'
        str += '  A -> aAB|Aa|%s\n' % X
        str += '  B -> b|bB\n'
        str += '  %s -> AB|b\n' % S
        str += '}'

        gerador = GeradorFormalismoGramatica(gramatica)
        self.assertEqual(gerador.gerar(), str)

    def test_gerar_formalismo_sem_sentenca_vazia(self):
        gramatica = Gramatica(
            [S, 'A'],
            ['a', 'b', 'c'],
            {
                S: ['aSc', 'A'],
                'A': ['b', 'bA']
            }
        )

        str = 'G = ({S, A}, {a, b, c}, P, %s)' % S
        str += '\nP = {\n'
        str += '  A -> b|bA\n'
        str += '  %s -> aSc|A\n' % S
        str += '}'

        gerador = GeradorFormalismoGramatica(gramatica)
        self.assertEqual(gerador.gerar(), str)