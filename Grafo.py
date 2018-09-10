from random import random
import collections

'''
Implementação de estrutura de grafos.

Mateus Rissi
'''
class Grafo:
    '''
    O próprio grafo.
    '''
    def __init__(self, dic_grafo=None):
        if dic_grafo is None:
            self.lista_de_vertices = {}
        else:
            self.lista_de_vertices = dic_grafo

    # Operações básicas

    '''
    Adiciona um vértice ao grafo.

    v (str): vértice para ser adicionado.
    '''
    def adiciona_vertice(self, v):
        if v in self.lista_de_vertices.keys():
            print('Vértice %s já existe!\n' % v)
            return False
        else:
            self.lista_de_vertices[v] = []
            print('Vértice %s adicionado ao grafo' % v)
            return True

    '''
    Remove um vértice do grafo.

    v (str): vértice para ser removido.
    '''
    def remove_vertice(self, v):
        if v not in self.lista_de_vertices.keys():
            print('Vértice %s não existe!\n' % v)
            return False
        else:
            self.lista_de_vertices.pop(v)
            for key in self.lista_de_vertices:
                if v in self.lista_de_vertices[key]:
                    self.lista_de_vertices[key].remove(v)
            return True

    '''
    Conecta dois vértices existentes do grafo.

    v1 (str): primeiro vértice.
    v2 (str): segundo vértice.
    '''
    def conecta(self, v1, v2):
        if v1 not in self.lista_de_vertices.keys():
            print('Vértice %s não existe!\n' % v1)
            return False
        if v2 not in self.lista_de_vertices.keys():
            print('Vértice %s não existe!\n' % v2)
            return False
        if v1 in self.adjacentes(v2):
            print('Aresta %s já está conectada com a aresta %s!\n' % (v1, v2))
        else:
            self.lista_de_vertices[v1].append(v2)
            self.lista_de_vertices[v2].append(v1)
            print('Aresta %s conectada com aresta %s!\n' % (v1, v2))
            return True

    '''
    Desconecta dois vértices existentes do grafo.

    v1 (str): primeiro vértice.
    v2 (str): segundo vértice.
    '''
    def desconecta(self, v1, v2):
        if v1 not in self.lista_de_vertices.keys():
            print('Vértice %s não existe!\n' % v1)
            return False
        if v2 not in self.lista_de_vertices.keys():
            print('Vértice %s não existe!\n' % v2)
            return False
        if v1 in self.adjacentes(v2):
            self.lista_de_vertices[v1].remove(v2)
            self.lista_de_vertices[v2].remove(v1)
            print('Aresta %s já não mais está conectada com a aresta %s!\n' % (v1, v2))
        else:
            print('Aresta %s não está conectada com a aresta %s!\n' % (v1, v2))
        return True

    '''
    Retorna a ordem do grafo.
    '''
    def ordem(self):
        return len(self.vertices())

    '''
    Retorna uma lista com os vértices do grafo.
    '''
    def vertices(self):
        return list(self.lista_de_vertices.keys())

    '''
    Retorna um vértice aleatório do grafo.
    '''
    def um_vertice(self):
        return random.choice(self.vertices())

    '''
    Retorna um conjunto com todos os vértices adjacentes à determinado vértice.

    v (str): determinado vértice.
    '''
    def adjacentes(self, v):
        if v not in self.vertices():
            print('Vértice %s não existe!\n' % v)
            return False
        else:
            return self.lista_de_vertices[v]

    '''
    Verifica e retorna o grau de determinado vértice.

    v (str): determinado vértice.
    '''
    def grau(self, v):
        if v not in self.vertices():
            print('Vértice %s não existe!\n' % v)
            return False
        else:
            adj = self.adjacentes(v)
            grau = len(adj) + adj.count(v)
            return grau

    # Ações derivadas

    '''
    Verifica se todos os vértices do grafo possuem o mesmo grau.
    '''
    def eh_regular(self):
        n = self.grau(self.um_vertice())
        for vertice in self.vertices():
            if self.grau(vertice) != n:
                return False
        return True

    '''
    Verifica se cada um dos vértices do grafo estão conectados a todos os outros vértices.
    '''
    def eh_completo(self):
        n = ((self.ordem()) - 1)
        for vertice in self.vertices():
            if self.grau(vertice) != n:
                return False
        return True

    '''
    Retorna um conjunto contendo todos os vértices do grafo que são transitivamente alcançáveis partindo-se de v.

    v (str): vértice de referência.
    '''
    def fecho_transitivo(self, v):
        novo_dict = []
        return self.__procura_fecho_transitivo(v, novo_dict)

    '''
    Método privado utilizado pelo método fecho_transitivo.

    v (str): vértice de referência.
    visitados (set): vértices já visitados.
    '''
    def __procura_fecho_transitivo(self, v, visitados):
        visitados.append(v)
        for v_adj in self.adjacentes(v):
            if v_adj not in visitados:
                self.__procura_fecho_transitivo(v_adj, visitados)
        return visitados

    '''
    Verifica se existe pelo menos um caminho entre cada par de vértices
    '''
    def eh_conexo(self):
        a = self.vertices()
        b = self.fecho_transitivo(self.um_vertice())
        if self.__compare(a, b):
            return True
        else:
            return False

    '''
    Método estático utilizado pelo método eh_conexo para comparar duas listas e retornar True se forem iguais
    '''
    @staticmethod
    def __compare(x, y):
        return collections.Counter(x) == collections.Counter(y)

    '''
    Verifica se o grafo é uma árvore, ou seja, se não possue ciclos e se é conexo.
    '''
    def eh_arvore(self):
        v = self.um_vertice()
        novo_dict = []
        if (self.eh_conexo is True) and (self.__ha_ciclo_com(v, v, novo_dict) is False):
            return True
        else:
            return False

    '''
    Método privado utilizado pelo método eh_arvore para verificar se v faz parte de algum ciclo no grafo.

    v (str): vértice que será testado contra o conjunto de vértices visitados.
    v_anterior (str): vértice de referência.
    visitados (set): conjunto de vértices visitados.
    '''
    def __ha_ciclo_com(self, v, v_anterior, visitados):
        if v in visitados:
            return True
        visitados.append(v)
        for v_adj in self.adjacentes(v):
            if v_adj != v_anterior:
                if self.__ha_ciclo_com(v_adj, v, visitados):
                    return True
        visitados.remove(v)
        return False

    '''
    Algoritmo usado para realizar uma busca em um grafo. O algoritmo
    inicia num nó raiz e explora tanto quanto possível cada um de seus
    ramos antes de retroceder (tomando um grafo com estrutura de árvore como exemplo).
    Complexidade O(n+m)/n = número de vértices e m = número de arestas.

    vertice (str): vértice raiz.
    '''
    def busca_em_profundidade(self, vertice):
        if vertice not in self.lista_de_vertices:
            print("Vértice não existe!\n")
        else:
            pilha = []
            visitados = []
            pilha.append(vertice)
            while pilha:
                vertice = pilha.pop()
                if vertice not in visitados:
                    visitados.append(vertice)
                    for aresta in self.lista_de_vertices[vertice]:
                        pilha. append(aresta)
            return visitados

if __name__ == "__main__":
    g_busca = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F', 'G'],
        'D': ['H', 'I'],
        'E': [],
        'F': [],
        'G': [],
        'H': ['J', 'L'],
        'I': [],
        'J': [],
        'L': []
    }

    g = Grafo(g_busca)
    print(g.busca_em_profundidade('A'))
