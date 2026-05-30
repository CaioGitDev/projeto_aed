# Testes unitários da ListaLigada e do No.

# Para executar estes testes, utilizar o comando: pytest testes/test_lista_ligada.py -v

import pytest
from src.estruturas import No, ListaLigada


# Testes para a classe No
class TestNo:
  def test_no_armazena_valor(self):
    no = No(valor=17)
    assert no.valor == 17
    assert no.proximo is None
    
  def test_no_aceita_ref_proximo(self):
    segundo_no = No(valor="segundo")
    primeiro_no = No(valor="primeiro", proximo=segundo_no)
    assert primeiro_no.proximo is segundo_no
    assert primeiro_no.proximo.valor == "segundo"
  
  def test_no_proximo_e_mutavel(self):
    no = No(1)
    no.proximo = No(2)
    assert no.proximo is not None
    assert no.proximo.valor == 2

  def test_repr_nao_segue_cadeia(self):
    # Importante: não deve causar recursão em listas longas.
    no = No(1, proximo=No(2, proximo=No(3)))
    assert "No(valor=1)" == repr(no)

# Testes para criação da lista ligada
class TestInicializacaoListaLigada:
  def test_lista_esta_vazia_ao_inicializar(self):
    nova_lista: ListaLigada[int] = ListaLigada()
    assert nova_lista.esta_vazia() == True
    assert nova_lista.tamanho == 0
    assert len(nova_lista) == 0
    
  def test_iteracao_em_lista_vazia_nao_produz_elementos(self):
    nova_lista: ListaLigada[int] = ListaLigada()
    assert list(nova_lista) == []

# Testes para o método inserir_inicio
class TestInserirInicio:
  def test_insere_em_lista_vazia(self):
    lista: ListaLigada[int] = ListaLigada()
    lista.inserir_inicio(10)
    assert lista.tamanho == 1
    assert lista.obter(0) == 10

  def test_inserir_inicio_coloca_no_topo(self):
    lista: ListaLigada[int] = ListaLigada()
    lista.inserir_inicio(1)
    lista.inserir_inicio(2)
    lista.inserir_inicio(3)
    # Ordem esperada: 3, 2, 1
    assert list(lista) == [3, 2, 1]

  def test_inserir_inicio_atualiza_cauda_em_lista_vazia(self):
    # Caso-limite: ao inserir no início numa lista vazia, a cauda
    # tem de passar a apontar para o mesmo nó.
    lista: ListaLigada[int] = ListaLigada()
    lista.inserir_inicio(7)
    lista.inserir_fim(8)  # Se a cauda estivesse mal, isto falharia
    assert list(lista) == [7, 8]
    
# Testes para o método inserir_fim
class TestInserirFim:
  def test_insere_em_lista_vazia(self):
    lista: ListaLigada[str] = ListaLigada()
    lista.inserir_fim("A")
    assert list(lista) == ["A"]

  def test_inserir_fim_acrescenta_ao_final(self):
    lista: ListaLigada[str] = ListaLigada()
    lista.inserir_fim("A")
    lista.inserir_fim("B")
    lista.inserir_fim("C")
    assert list(lista) == ["A", "B", "C"]
    assert lista.tamanho == 3
  
# Testes para inserir em posição específica
# TODO
  
# Testes para remover por posição
# TODO

# Testes para remover por valor
# TODO
    
    
    
    
    
    
    
    
    