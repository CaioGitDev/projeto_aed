"""
Grafo representado por lista de adjacência.
 
Complexidades (V = nº de nós, E = nº de arestas)
-----------------------------------------------
- adicionar_no    : O(V)   (verifica duplicação)
- adicionar_aresta: O(V)   (localiza as entradas dos nós)
- remover_aresta  : O(V + E)
- remover_no      : O(V + E)
- vizinhos        : O(V)
- existe_no       : O(V)
- nos             : O(V)
"""


from __future__ import annotations
from .lista_ligada import ListaLigada

class NoInexistenteError(Exception):
  """Nó não existe no grafo."""
  
class _EntradaAdjacencia:
  # Classe auxiliar para representar a entrada de um nó na lista de adjacência.
  # associa um nó a uma lista de seus vizinhos.
  __slots__ = ("nome", "vizinhos")
  
  def __init__(self, nome: str) -> None:
    self.nome: str = nome
    self.vizinhos: ListaLigada[str] = ListaLigada()
  
  def __repr__(self) -> str:
    return f"_EntradaAdjacencia(nome={self.nome!r}, vizinhos={list(self.vizinhos)})"
  
  
class Grafo:
  # Grafo não ponderado representado por lista de adjacencia
  # inputs
  # dirigido: bool
  # se True as arestas tem sentido unico, se false cada arresta adicionada entre A e B implica em uma aresta de B para A.
  
  __slots__ = ("_adjacencias", "_dirigido")
  
  def __init__(self, dirigido: bool = False) -> None:
    # lista ligada de _EntradaAdjacencia, uma por no do grafo
    self._adjacencias: ListaLigada[_EntradaAdjacencia] = ListaLigada()
    self._dirigido: bool = dirigido
    
  # pripriedades
  @property
  def dirigido(self) -> bool:
    # indica se o grafo é dirigido ou não O(1)
    return self._dirigido
  
  @property
  def numero_nos(self) -> int:
    # número de nós no grafo O(1)
    return self._adjacencias.tamanho
  
  # operações
  def adicionar_no(self, nome: str) -> None:
    # adiciona um no no grafo, se ja existir um no com o mesmo nome, nao faz nada O(V)
    if self._procurar_entrada(nome) is not None:
      return
    
    self._adjacencias.inserir_fim(_EntradaAdjacencia(nome))
    
  def adicionar_aresta(self, origem: str, destino: str) -> None:
    # adiciona uma aresta entre origem e destino
    # os nos sao criados automaticamente se nao existirem O(V)
    # em grafos nao dirigidos, a aresta é adicionada em ambos os sentidos
    self.adicionar_no(origem)
    self.adicionar_no(destino)
    
    self._ligar(origem, destino)
    if not self._dirigido:
      self._ligar(destino, origem)
      
      
  # remover
  def remover_aresta(self, origem: str, destino: str) -> None:
    # remove aresta entre origem e destino, se existir O(V + E)
    # em grafos nao dirigidos, a aresta é removida em ambos os sentidos
    self._exigir_no(origem)
    self._exigir_no(destino)
    
    self._desligar(origem, destino)
    if not self._dirigido:
      self._desligar(destino, origem)
      
  def remover_no(self, nome: str) -> None:
    # remove um no do grafo se existir O(V + E)
    # remove a entrada do nó e remove todas as arestas associadas a ele
    entrada = self._procurar_entrada(nome)
    if entrada is None:
      raise NoInexistenteError(f"Nó {nome!r} não existe no grafo.")
    
    # remover a entrada do nó
    self._adjacencias.remover_valor(entrada)
    
    # remover arestas associadas a ele
    for entradas in self._adjacencias:
      if nome in entradas.vizinhos:
        entradas.vizinhos.remover_valor(nome)
    
  
  # consultas
  def existe_no(self, nome: str) -> bool:
    #verifica se o no existe no grafo O(V)
    return self._procurar_entrada(nome) is not None
  
  def vizinhos(self, nome: str) -> ListaLigada[str]:
    # retorna uma lista ligada com os vizinhos do no indicado O(V)
    # Lança NoInexistenteError se o nó não existir.
    # a lista retonrada é uma cópia, modificações nela não afetam o grafo
    entrada = self._procurar_entrada(nome)
    if entrada is None:
      raise NoInexistenteError(f"Nó {nome!r} não existe no grafo.")
    copia_vizinhos: ListaLigada[str] = ListaLigada()
    for vizinho in entrada.vizinhos:
      copia_vizinhos.inserir_fim(vizinho)
    return copia_vizinhos
  
  # nos
  def nos(self) -> ListaLigada[str]:
    # retorna uma lista ligada com os nomes de todos os nós do grafo O(V)
    lista_nos: ListaLigada[str] = ListaLigada()
    for entrada in self._adjacencias:
      lista_nos.inserir_fim(entrada.nome)
    return lista_nos
  
  def existe_aresta(self, origem: str, destino: str) -> bool:
    # indica se existe uma aresta entre origem e destino O(V)
    # Lança NoInexistenteError se algum dos nós não existir.
    entrada_origem = self._procurar_entrada(origem)
    if entrada_origem is None:
      raise NoInexistenteError(f"Nó {origem!r} não existe no grafo.")
    return destino in entrada_origem.vizinhos
  
  # métodos auxiliares
  def _procurar_entrada(self, nome: str) -> _EntradaAdjacencia | None:
    # localiza a entrada de adjacência de um no, ou retorna None se não encontrar O(V)
    for entrada in self._adjacencias:
      if entrada.nome == nome:
        return entrada
    return None
  
  def _exigir_no(self, nome: str) -> None:
    # localiza a entrada de um no, ou lança NoInexistenteError se não encontrar O(V)
    entrada = self._procurar_entrada(nome)
    if entrada is None:
      raise NoInexistenteError(f"Nó {nome!r} não existe no grafo.")
    return entrada
  
  def _ligar(self, origem: str, destino: str) -> None:
    # acrescenta destino à lista de vizinhos de origem sem duplicar O(V)
    entrada_origem = self._procurar_entrada(origem)
    assert entrada_origem is not None  # Garantir que a entrada existe
    if destino not in entrada_origem.vizinhos:
      entrada_origem.vizinhos.inserir_fim(destino)
      
  def _desligar(self, origem: str, destino: str) -> None:
    # remove destino da lista de vizinhos de origem se existir O(V + E)
    entrada_origem = self._procurar_entrada(origem)
    assert entrada_origem is not None  # Garantir que a entrada existe
    if destino in entrada_origem.vizinhos:
      entrada_origem.vizinhos.remover_valor(destino)
    
    
  def __repr__(self) -> str:
    tipo = "dirigido" if self._dirigido else "não dirigido"
    linhas = []
    for entrada in self._adjacencias:
      vizinhos = ", ".join(entrada.vizinhos)
      linhas.append(f"  {entrada.nome} -> [{vizinhos}]")
    corpo = "\n".join(linhas)
    return f"Grafo ({tipo}, {self.numero_nos} nós):\n{corpo}"
  
  
