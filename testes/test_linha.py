# Testes para a classe Linha
# pytest testes/test_linha.py -v

import pytest
 
from src.dominio.linha import (
  Linha,
  ParagemDuplicadaError,
  ParagemNaoEncontradaError,
)
from src.dominio.paragem import Paragem
from src.dominio.passageiro import Passageiro
 
 
def _nomes(lista_ligada):
  return [p.nome for p in lista_ligada]
 
 
class TestConstrucao:
  def test_linha_recem_criada_esta_vazia(self):
    linha = Linha("Salvaterra -> Coruche")
    assert linha.nome == "Salvaterra -> Coruche"
    assert linha.numero_paragens == 0
    assert linha.esta_vazia()

  def test_nome_e_limpo_de_espacos(self):
    linha = Linha("  Coruche -> Salvaterra  ")
    assert linha.nome == "Coruche -> Salvaterra"

  def test_nome_vazio_lanca_erro(self):
    with pytest.raises(ValueError):
      Linha("")

  def test_nome_so_com_espacos_lanca_erro(self):
    with pytest.raises(ValueError):
      Linha("   ")
      
      
# inserir paragem
class TestInserirParagem:
  def test_inserir_no_fim_por_omissao(self):
    linha = Linha("Salvaterra -> Coruche")
    linha.inserir_paragem(Paragem("Salvaterra"))
    linha.inserir_paragem(Paragem("Coruche"))
    assert _nomes(linha.listar_percurso()) == ["Salvaterra", "Coruche"]

  def test_inserir_no_inicio(self):
    linha = Linha("Salvaterra -> Santarem")
    linha.inserir_paragem(Paragem("Santarem"))
    linha.inserir_paragem(Paragem("Marinhais"))
    linha.inserir_paragem(Paragem("Muge"), posicao=0)
    assert _nomes(linha.listar_percurso()) == [
      "Muge",
      "Santarem",
      "Marinhais",
    ]

  def test_inserir_em_posicao_intermedia(self):
    linha = Linha("L1")
    for nome in ["A", "B", "D"]:
      linha.inserir_paragem(Paragem(nome))
    linha.inserir_paragem(Paragem("C"), posicao=2)
    assert _nomes(linha.listar_percurso()) == ["A", "B", "C", "D"]

  def test_paragem_duplicada_lanca_erro(self):
    linha = Linha("L1")
    linha.inserir_paragem(Paragem("Rossio"))
    with pytest.raises(ParagemDuplicadaError):
      linha.inserir_paragem(Paragem("Rossio"))

  def test_posicao_invalida_lanca_erro(self):
    linha = Linha("L1")
    linha.inserir_paragem(Paragem("A"))
    with pytest.raises(IndexError):
      linha.inserir_paragem(Paragem("B"), posicao=5)
    with pytest.raises(IndexError):
      linha.inserir_paragem(Paragem("C"), posicao=-1)
      
class TestConstruirGrafo:
  def test_linha_vazia_produz_grafo_sem_nos(self):
    linha = Linha("L1")
    g = linha.construir_grafo()
    assert g.numero_nos == 0

  def test_linha_com_uma_paragem(self):
    linha = Linha("L1")
    linha.inserir_paragem(Paragem("Solo"))
    g = linha.construir_grafo()
    assert g.numero_nos == 1
    assert g.existe_no("Solo")
    assert list(g.vizinhos("Solo")) == []

  def test_paragens_consecutivas_ficam_ligadas(self):
    linha = Linha("L1")
    for nome in ["A", "B", "C", "D"]:
      linha.inserir_paragem(Paragem(nome))
    g = linha.construir_grafo()
    assert g.numero_nos == 4
    # Cada paragem liga à anterior e à seguinte (não dirigido).
    assert set(g.vizinhos("A")) == {"B"}
    assert set(g.vizinhos("B")) == {"A", "C"}
    assert set(g.vizinhos("C")) == {"B", "D"}
    assert set(g.vizinhos("D")) == {"C"}

  def test_grafo_e_independente_da_linha(self):
    # Após construir o grafo, alterações à linha não afetam o
    # grafo já produzido (e vice-versa).
    linha = Linha("L1")
    linha.inserir_paragem(Paragem("A"))
    linha.inserir_paragem(Paragem("B"))
    g = linha.construir_grafo()
    linha.inserir_paragem(Paragem("C"))
    assert g.numero_nos == 2 
    
    
  # caso integrado
  
  class TestCenarioIntegrado:
    def test_contruir_operar_e_inspecionar(self):
      linha = Linha("Salvaterra -> Santarem")
      
      # construir linha
      for nome in ["Salvaterra", "Marinhais", "Muge", "Santarem"]:
        linha.inserir_paragem(Paragem(nome))
      assert linha.numero_paragens == 4
      
      # inserir no meio
      linha.inserir_paragem(Paragem("Foros de salvaterra"), posicao=1)
      assert _nomes(linha.listar_percurso()) == [
        "Salvaterra",
        "Foros de salvaterra",
        "Marinhais",
        "Muge",
        "Santarem",
      ]
      
      # adicionar passageiros
      muge = linha.obter_paragem("Muge")
      muge.adicionar_passageiro(Passageiro("Catarina"))
      muge.adicionar_passageiro(Passageiro("Sofia"))
      assert linha.obter_paragem("Muge").numero_em_espera() == 2
      
      # remover paragem
      linha.remover_paragem("Foros de salvaterra")
      assert linha.numero_paragens == 4
      assert not linha.contem_paragem("Foros de salvaterra")
      
      # construir grafo
      grafo = linha.construir_grafo()
      assert grafo.numero_nos == 4
      assert set(grafo.vizinhos("Muge")) == {"Marinhais","Santarem"} 