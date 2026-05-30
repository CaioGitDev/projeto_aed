"""
Pesquisa em largura Breadth-First Search (BFS) sobre grafo.
 
Implementação da BFS clássica, recorrendo às estruturas de dados do
projeto: uma `Fila` para a frente de exploração e `ListaLigada` para o
controlo de visitados e reconstrução do caminho. Esta é uma
ilustração intencional da reutilização das estruturas da Fase 1:
a `Fila`, originalmente criada para os passageiros, serve agora como
componente fundamental de um algoritmo de pesquisa.
 
O algoritmo devolve o caminho com o menor número de arestas (paragens)
entre duas paragens no grafo. Em grafos não-ponderados (o nosso caso),
a BFS é o algoritmo natural para esta tarefa, sendo Dijkstra
desnecessariamente complexo neste contexto.
 
Complexidade
------------
- Tempo : O((V + E) · V) — o fator V adicional resulta da consulta
          linear nas estruturas de visitados/predecessores (ausência
          deliberada de `dict` nativo na implementação de raiz). Em
          grafos densos a complexidade aproxima-se de O(V³); para os
          grafos do âmbito do projeto (dezenas de paragens) é
          irrelevante.
- Espaço: O(V), para visitados e predecessores.
"""
 
from __future__ import annotations
 
from src.estruturas.fila import Fila
from src.estruturas.grafo import Grafo, NoInexistenteError
from src.estruturas.lista_ligada import ListaLigada
 
class _EntradaPredecessor:
  """
  Associa um nó ao nó pelo qual foi alcançado durante a BFS.

  Uma origem terá `predecessor = None`. Classe interna a este módulo.
  """

  __slots__ = ("no", "predecessor")

  def __init__(self, no: str, predecessor: str | None) -> None:
    self.no: str = no
    self.predecessor: str | None = predecessor


def _procurar_predecessor(
  entradas: ListaLigada[_EntradaPredecessor], no: str
) -> _EntradaPredecessor | None:
  """Localiza linearmente a entrada de predecessores de um nó."""
  for entrada in entradas:
    if entrada.no == no:
      return entrada
  return None
 
 
def bfs_caminho(grafo: Grafo, origem: str, destino: str) -> ListaLigada[str] | None:
  """
  Calcula o caminho com menor número de arestas entre `origem` e
  `destino` no `grafo`, recorrendo a Breadth-First Search.

  Parâmetros
  ----------
  grafo : Grafo
      Grafo onde a pesquisa é realizada.
  origem : str
      Nome do nó de partida.
  destino : str
      Nome do nó de chegada.

  Devolve
  -------
  ListaLigada[str] | None
      Sequência de nomes de nós do caminho mais curto, da origem ao
      destino inclusive. Se origem e destino coincidirem, devolve uma
      lista com um único elemento (caminho de comprimento zero).
      Devolve `None` se não houver caminho.

  Exceções
  --------
  NoInexistenteError
      Se a origem ou o destino não existirem no grafo.
  """
  # Validações de entrada — falhar cedo e com clareza.
  if not grafo.existe_no(origem):
    raise NoInexistenteError(f"O nó de origem {origem!r} não existe no grafo.")
  if not grafo.existe_no(destino):
    raise NoInexistenteError(f"O nó de destino {destino!r} não existe no grafo.")

  # Caso trivial: origem e destino coincidem.
  if origem == destino:
    caminho: ListaLigada[str] = ListaLigada()
    caminho.inserir_fim(origem)
    return caminho

  # Estruturas de controlo.
  visitados: ListaLigada[str] = ListaLigada()
  predecessores: ListaLigada[_EntradaPredecessor] = ListaLigada()
  frente: Fila[str] = Fila()

  # Inicialização.
  visitados.inserir_fim(origem)
  predecessores.inserir_fim(_EntradaPredecessor(origem, None))
  frente.enfileirar(origem)

  encontrado = False

  # Iteração principal: explora a frente de pesquisa em largura.
  while not frente.esta_vazia():
    atual = frente.desenfileirar()

    for vizinho in grafo.vizinhos(atual):
      if vizinho in visitados:
        continue
      visitados.inserir_fim(vizinho)
      predecessores.inserir_fim(_EntradaPredecessor(vizinho, atual))
      if vizinho == destino:
        encontrado = True
        # Termina a expansão; reconstrução do caminho a seguir.
        # Não retornamos imediatamente porque a clareza ganha
        # com a separação entre a fase de exploração e a fase
        # de reconstrução compensa o custo (nulo neste ponto).
        frente = Fila()  # Esvazia a frente para sair do while.
        break
      # Caso geral: enfileirar para expansão futura.
      frente.enfileirar(vizinho)
    if encontrado:
      break

  if not encontrado:
    return None

  # Reconstrução do caminho percorrendo predecessores do destino até
  # à origem, e invertendo no final.
  caminho_invertido: ListaLigada[str] = ListaLigada()
  no_atual: str | None = destino
  while no_atual is not None:
    caminho_invertido.inserir_fim(no_atual)
    entrada = _procurar_predecessor(predecessores, no_atual)
    # A entrada existe sempre (construímo-la durante a expansão).
    assert entrada is not None
    no_atual = entrada.predecessor

  # Inverter para obter origem -> destino.
  caminho: ListaLigada[str] = ListaLigada()
  for nome in caminho_invertido:
    caminho.inserir_inicio(nome)
  return caminho