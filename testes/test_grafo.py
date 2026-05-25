"""
Testes unitários do `Grafo`.
Execução:
    pytest testes/test_grafo.py -v
"""
 
import pytest
 
from src.estruturas.grafo import Grafo, NoInexistenteError

def _conjunto(lista_ligada):
  """Auxiliar: converte uma ListaLigada num set, para comparação de
  vizinhanças sem dependência da ordem de inserção."""
  return set(lista_ligada)


class TestAdicionarNo:
  def test_grafo_recem_criado_nao_tem_nos(self):
    g = Grafo()
    assert g.numero_nos == 0

  def test_adicionar_no(self):
    g = Grafo()
    g.adicionar_no("Rossio")
    assert g.existe_no("Rossio")
    assert g.numero_nos == 1

  def test_adicionar_no_e_idempotente(self):
    g = Grafo()
    g.adicionar_no("Rossio")
    g.adicionar_no("Rossio")
    # Não deve duplicar.
    assert g.numero_nos == 1
    
    
# adicao arestas
class TestAdicionarAresta:
  def test_aresta_cria_nos_automaticamente(self):
    grafo = Grafo()
    grafo.adicionar_aresta("A", "B")
    assert grafo.existe_no("A")
    assert grafo.existe_no("B")
    assert grafo.numero_nos == 2
    
  def test_aresta_nao_dirigida_e_bidirecional(self):
    grafo = Grafo(dirigido=False)
    grafo.adicionar_aresta("porto", "lisboa")
    assert grafo.existe_aresta("porto", "lisboa")
    assert grafo.existe_aresta("lisboa", "porto")

  def test_aresta_dirigida_e_unidirecional(self):
    g = Grafo(dirigido=True)
    g.adicionar_aresta("A", "B")
    assert g.existe_aresta("A", "B")
    assert not g.existe_aresta("B", "A")

  def test_arestas_duplicadas_sao_ignoradas(self):
    g = Grafo()
    g.adicionar_aresta("A", "B")
    g.adicionar_aresta("A", "B")
    vizinhos_a = list(g.vizinhos("A"))
    assert vizinhos_a.count("B") == 1

  def test_vizinhanca_multipla(self):
    g = Grafo()
    g.adicionar_aresta("A", "B")
    g.adicionar_aresta("A", "C")
    g.adicionar_aresta("A", "D")
    assert _conjunto(g.vizinhos("A")) == {"B", "C", "D"}

class TestRemocao:
  def test_remover_aresta_nao_dirigida(self):
    g = Grafo()
    g.adicionar_aresta("A", "B")
    g.remover_aresta("A", "B")
    assert not g.existe_aresta("A", "B")
    assert not g.existe_aresta("B", "A")
    # Os nós permanecem.
    assert g.existe_no("A")
    assert g.existe_no("B")

  def test_remover_aresta_dirigida(self):
    g = Grafo(dirigido=True)
    g.adicionar_aresta("A", "B")
    g.adicionar_aresta("B", "A")
    g.remover_aresta("A", "B")
    assert not g.existe_aresta("A", "B")
    # A aresta no sentido contrário mantém-se.
    assert g.existe_aresta("B", "A")

  def test_remover_no_remove_referencias(self):
    g = Grafo()
    g.adicionar_aresta("A", "B")
    g.adicionar_aresta("C", "B")
    g.adicionar_aresta("B", "D")
    # B é vizinho de A e de C, e tem D como vizinho.
    g.remover_no("B")
    assert not g.existe_no("B")
    # As referências a B devem ter desaparecido das vizinhanças.
    assert "B" not in list(g.vizinhos("A"))
    assert "B" not in list(g.vizinhos("C"))
    assert g.existe_no("D")

  def test_remover_no_inexistente_lanca_erro(self):
    g = Grafo()
    with pytest.raises(NoInexistenteError):
      g.remover_no("X")

  def test_remover_aresta_com_no_inexistente_lanca_erro(self):
    g = Grafo()
    g.adicionar_no("A")
    with pytest.raises(NoInexistenteError):
      g.remover_aresta("A", "X")

class TestConsultas:
  def test_nos_devolve_todos(self):
    g = Grafo()
    for nome in ["A", "B", "C"]:
      g.adicionar_no(nome)
    assert _conjunto(g.nos()) == {"A", "B", "C"}

  def test_vizinhos_de_no_isolado_e_vazio(self):
    g = Grafo()
    g.adicionar_no("A")
    assert list(g.vizinhos("A")) == []

  def test_vizinhos_de_no_inexistente_lanca_erro(self):
    g = Grafo()
    with pytest.raises(NoInexistenteError):
      g.vizinhos("X")

  def test_existe_aresta_de_no_inexistente_lanca_erro(self):
    g = Grafo()
    with pytest.raises(NoInexistenteError):
      g.existe_aresta("X", "Y")

  def test_vizinhos_devolve_copia_defensiva(self):
    # Alterar a lista devolvida não deve afetar o grafo.
    g = Grafo()
    g.adicionar_aresta("A", "B")
    copia = g.vizinhos("A")
    copia.inserir_fim("FALSO")
    assert "FALSO" not in list(g.vizinhos("A"))
    

class TestCenarioIntegrado:
  """
  Cenário aproximado de uso real: construção de uma pequena rede de
  paragens com ligações entre elas.
  """

  def test_rede_de_paragens(self):
    # Topologia:
    #   Rossio --- Restauradores --- Marquês
    #     |                            |
    #   Cais Sodré ----------------- Saldanha
    g = Grafo(dirigido=False)
    g.adicionar_aresta("Rossio", "Restauradores")
    g.adicionar_aresta("Restauradores", "Marquês")
    g.adicionar_aresta("Rossio", "Cais Sodré")
    g.adicionar_aresta("Marquês", "Saldanha")
    g.adicionar_aresta("Cais Sodré", "Saldanha")

    assert g.numero_nos == 5

    # Rossio liga a Restauradores e a Cais Sodré.
    assert _conjunto(g.vizinhos("Rossio")) == {"Restauradores", "Cais Sodré"}

    # Saldanha liga a Marquês e a Cais Sodré.
    assert _conjunto(g.vizinhos("Saldanha")) == {"Marquês", "Cais Sodré"}

    # Encerramento de uma paragem: remover Restauradores.
    g.remover_no("Restauradores")
    assert g.numero_nos == 4
    assert "Restauradores" not in list(g.vizinhos("Rossio"))
    assert "Restauradores" not in list(g.vizinhos("Marquês"))