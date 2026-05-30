"""
Testes unitários do bfs_caminho
pytest testes/test_pesquisa.py -v
"""

import pytest

from src.algoritmos.pesquisa import bfs_caminho
from src.dominio.linha import Linha
from src.dominio.paragem import Paragem
from src.estruturas.grafo import Grafo, NoInexistenteError


class TestCasosTriviais:
  def test_origem_igual_destino_devolve_lista_com_um_elemento(self):
    g = Grafo()
    g.adicionar_no("A")
    caminho = bfs_caminho(g, "A", "A")
    assert caminho is not None
    assert list(caminho) == ["A"]

  def test_vizinho_direto(self):
    g = Grafo()
    g.adicionar_aresta("A", "B")
    caminho = bfs_caminho(g, "A", "B")
    assert caminho is not None
    assert list(caminho) == ["A", "B"]

  def test_caminho_em_grafo_linear(self):
    # A -- B -- C -- D
    g = Grafo()
    g.adicionar_aresta("A", "B")
    g.adicionar_aresta("B", "C")
    g.adicionar_aresta("C", "D")
    caminho = bfs_caminho(g, "A", "D")
    assert caminho is not None
    assert list(caminho) == ["A", "B", "C", "D"]



# caminho MAIS CURTO
class TestCaminhoMaisCurto:
  def test_escolhe_atalho_em_grafo_com_alternativas(self):
    # Topologia:
    #   A -- B -- C -- D
    #   |              |
    #   +------E-------+
    #
    # De A até D existem dois caminhos:
    #  - A-B-C-D (3 arestas)
    #  - A-E-D   (2 arestas)
    # A BFS deve escolher o segundo.
    g = Grafo()
    g.adicionar_aresta("A", "B")
    g.adicionar_aresta("B", "C")
    g.adicionar_aresta("C", "D")
    g.adicionar_aresta("A", "E")
    g.adicionar_aresta("E", "D")

    caminho = bfs_caminho(g, "A", "D")
    assert caminho is not None
    # O caminho mais curto tem 3 nós (2 arestas).
    assert len(caminho) == 3
    assert list(caminho) == ["A", "E", "D"]

  def test_ciclo_nao_impede_terminacao(self):
    # Grafo cíclico: A-B-C-A.
    g = Grafo()
    g.adicionar_aresta("A", "B")
    g.adicionar_aresta("B", "C")
    g.adicionar_aresta("C", "A")
    caminho = bfs_caminho(g, "A", "C")
    assert caminho is not None
    # Tanto A-B-C como A-C têm validade; a BFS deve escolher o mais
    # curto, que é A-C (uma única aresta).
    assert list(caminho) == ["A", "C"]


class TestSemCaminho:
  def test_componentes_desconexas_devolve_none(self):
    # Dois componentes desconexos: {A,B} e {C,D}.
    g = Grafo()
    g.adicionar_aresta("A", "B")
    g.adicionar_aresta("C", "D")
    assert bfs_caminho(g, "A", "C") is None
    assert bfs_caminho(g, "B", "D") is None

  def test_no_isolado(self):
    # X isolado; outros conectados.
    g = Grafo()
    g.adicionar_aresta("A", "B")
    g.adicionar_no("X")
    assert bfs_caminho(g, "A", "X") is None
    assert bfs_caminho(g, "X", "B") is None


class TestErros:
  def test_origem_inexistente_lanca_erro(self):
    g = Grafo()
    g.adicionar_no("A")
    with pytest.raises(NoInexistenteError):
      bfs_caminho(g, "FANTASMA", "A")

  def test_destino_inexistente_lanca_erro(self):
    g = Grafo()
    g.adicionar_no("A")
    with pytest.raises(NoInexistenteError):
      bfs_caminho(g, "A", "FANTASMA")


class TestGrafoDirigido:
  def test_arestas_dirigidas_respeitadas(self):
    # Em grafo dirigido, só seguimos no sentido das arestas.
    g = Grafo(dirigido=True)
    g.adicionar_aresta("A", "B")
    g.adicionar_aresta("B", "C")
    # A -> C via B existe.
    caminho = bfs_caminho(g, "A", "C")
    assert caminho is not None
    assert list(caminho) == ["A", "B", "C"]
    # C -> A não existe (sem aresta no sentido inverso).
    assert bfs_caminho(g, "C", "A") is None


class TestIntegracaoLinha:
  def test_pesquisa_sobre_linha_constroi_caminho_correto(self):
    # Construir uma linha real e calcular percursos sobre o grafo
    # dela derivado.
    linha = Linha("Linha 728")
    for nome in ["Cais Sodré", "Rossio", "Restauradores", "Marquês", "Saldanha"]:
      linha.inserir_paragem(Paragem(nome))
    g = linha.construir_grafo()

    # Percurso completo de extremo a extremo.
    caminho = bfs_caminho(g, "Cais Sodré", "Saldanha")
    assert caminho is not None
    assert list(caminho) == [
      "Cais Sodré",
      "Rossio",
      "Restauradores",
      "Marquês",
      "Saldanha",
    ]

  def test_caminho_intermedio(self):
    linha = Linha("Linha 728")
    for nome in ["A", "B", "C", "D", "E"]:
      linha.inserir_paragem(Paragem(nome))
    g = linha.construir_grafo()
    caminho = bfs_caminho(g, "B", "D")
    assert caminho is not None
    assert list(caminho) == ["B", "C", "D"]