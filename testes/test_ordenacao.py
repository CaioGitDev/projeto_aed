# testes para os algoritmos de ordenação
# pytest testes/test_ordenacao.py -v

from dataclasses import dataclass
 
import pytest
 
from src.algoritmos.ordenacao import bubble_sort, insertion_sort, selection_sort
from src.dominio.paragem import Paragem
from src.dominio.passageiro import Passageiro
from src.estruturas.lista_ligada import ListaLigada

ALGORITMOS = [bubble_sort, insertion_sort, selection_sort]
 
 
def _lista(*elementos):
    ll = ListaLigada()
    for e in elementos:
        ll.inserir_fim(e)
    return ll
  
# injeta os algoritmos de ordenação nos testes
@pytest.mark.parametrize("algoritmo", ALGORITMOS)
class TestCasosCanonicos:
  def test_lista_aleatoria(self, algoritmo):
    entrada = _lista(5, 2, 8, 1, 9, 3, 7, 4, 6)
    resultado = algoritmo(entrada)
    assert list(resultado) == [1, 2, 3, 4, 5, 6, 7, 8, 9]

  def test_lista_ja_ordenada(self, algoritmo):
    entrada = _lista(1, 2, 3, 4, 5)
    resultado = algoritmo(entrada)
    assert list(resultado) == [1, 2, 3, 4, 5]

  def test_lista_decrescente(self, algoritmo):
    entrada = _lista(5, 4, 3, 2, 1)
    resultado = algoritmo(entrada)
    assert list(resultado) == [1, 2, 3, 4, 5]

  def test_lista_com_duplicados(self, algoritmo):
    entrada = _lista(3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5)
    resultado = algoritmo(entrada)
    assert list(resultado) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
    
@pytest.mark.parametrize("algoritmo", ALGORITMOS)
class TestCasosLimite:
  def test_lista_vazia(self, algoritmo):
    resultado = algoritmo(_lista())
    assert list(resultado) == []

  def test_lista_com_um_elemento(self, algoritmo):
    resultado = algoritmo(_lista(42))
    assert list(resultado) == [42]

  def test_todos_iguais(self, algoritmo):
    resultado = algoritmo(_lista(7, 7, 7, 7))
    assert list(resultado) == [7, 7, 7, 7]
    
@pytest.mark.parametrize("algoritmo", ALGORITMOS)
class TestImutabilidade:
  def test_entrada_permanece_inalterada(self, algoritmo):
    entrada = _lista(3, 1, 4, 1, 5)
    original = list(entrada)
    _ = algoritmo(entrada)
    assert list(entrada) == original

  def test_resultado_e_lista_ligada_diferente(self, algoritmo):
    entrada = _lista(2, 1)
    resultado = algoritmo(entrada)
    assert resultado is not entrada
    
@pytest.mark.parametrize("algoritmo", ALGORITMOS)
class TestOrdemInversa:
  def test_reverso_decrescente(self, algoritmo):
    entrada = _lista(3, 1, 4, 1, 5, 9, 2, 6)
    resultado = algoritmo(entrada, reverso=True)
    assert list(resultado) == [9, 6, 5, 4, 3, 2, 1, 1]
    
# Chave personalizada
@dataclass
class _Item:
    """Tipo auxiliar para testes de chave personalizada."""
    rotulo: str
    valor: int
 
 
@pytest.mark.parametrize("algoritmo", ALGORITMOS)
class TestChavePersonalizada:
  def test_ordenar_por_atributo(self, algoritmo):
    entrada = _lista(
      _Item("c", 3),
      _Item("a", 1),
      _Item("b", 2),
    )
    resultado = algoritmo(entrada, chave=lambda item: item.valor)
    assert [i.rotulo for i in resultado] == ["a", "b", "c"]

  def test_ordenar_por_atributo_reverso(self, algoritmo):
    entrada = _lista(
      _Item("c", 3),
      _Item("a", 1),
      _Item("b", 2),
    )
    resultado = algoritmo(
      entrada, chave=lambda item: item.valor, reverso=True
    )
    assert [i.rotulo for i in resultado] == ["c", "b", "a"]
    
# exemplo de aplicação
@pytest.mark.parametrize("algoritmo", ALGORITMOS)
class TestOrdenacaoDeParagens:
  """
  Os três algoritmos devem permitir ordenar paragens pelos dois
  critérios exigidos pelo enunciado:
  - por nome (lexicográfica);
  - por número de passageiros em espera.
  """

  @staticmethod
  def _construir_paragens():
    rossio = Paragem("Rossio")
    marques = Paragem("Marquês")
    cais = Paragem("Cais Sodré")

    # Popular as filas com quantidades distintas.
    for nome in ["Ana", "Bruno"]:
      rossio.adicionar_passageiro(Passageiro(nome))
    marques.adicionar_passageiro(Passageiro("Carla"))
    for nome in ["Diogo", "Eva", "Filipe"]:
      cais.adicionar_passageiro(Passageiro(nome))

    # Devolve em ordem propositadamente caótica.
    return _lista(rossio, marques, cais)

  def test_ordenar_paragens_por_nome(self, algoritmo):
    paragens = self._construir_paragens()
    resultado = algoritmo(paragens, chave=lambda p: p.nome)
    # Cais Sodré < Marquês < Rossio (lexicográfico).
    assert [p.nome for p in resultado] == ["Cais Sodré", "Marquês", "Rossio"]

  def test_ordenar_paragens_por_passageiros_crescente(self, algoritmo):
    paragens = self._construir_paragens()
    resultado = algoritmo(paragens, chave=lambda p: p.numero_em_espera())
    assert [p.numero_em_espera() for p in resultado] == [1, 2, 3]

  def test_ordenar_paragens_por_passageiros_decrescente(self, algoritmo):
    paragens = self._construir_paragens()
    resultado = algoritmo(
      paragens, chave=lambda p: p.numero_em_espera(), reverso=True
    )
    assert [p.numero_em_espera() for p in resultado] == [3, 2, 1]
    
class TestEstabilidade:
  """
  A estabilidade garante que elementos com a mesma chave preservam a
  ordem relativa de entrada. Bubble e Insertion são estáveis;
  Selection (na implementação clássica) não é.
  """

  @pytest.mark.parametrize("algoritmo", [bubble_sort, insertion_sort])
  def test_bubble_e_insertion_sao_estaveis(self, algoritmo):
    # Itens com chaves iguais e rótulos que permitem distinguir a
    # ordem original.
    entrada = _lista(
      _Item("primeiro_A", 1),
      _Item("primeiro_B", 2),
      _Item("segundo_A", 1),
      _Item("segundo_B", 2),
      _Item("terceiro_A", 1),
    )
    resultado = algoritmo(entrada, chave=lambda item: item.valor)
    rotulos = [item.rotulo for item in resultado]
    # Entre os de valor 1, a ordem original deve ser preservada.
    rotulos_de_1 = [r for r in rotulos if r.endswith("_A")]
    assert rotulos_de_1 == ["primeiro_A", "segundo_A", "terceiro_A"]
    
class TestOtimizacaoBubble:
  def test_lista_ja_ordenada_termina_cedo(self):
    # Espia o número de comparações para verificar que o early exit
    # é tomado. Numa lista já ordenada, deve haver apenas uma
    # passagem completa (n-1 comparações).
    contador = {"comparacoes": 0}

    def chave_contadora(x):
      contador["comparacoes"] += 1
      return x

    entrada = _lista(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    _ = bubble_sort(entrada, chave=chave_contadora)

    # Em Bubble Sort otimizado: 1ª passagem = 2*(n-1) chamadas a
    # `chave` (duas por comparação). Como n=10, são 18. Sem
    # otimização, seriam 2 * (n-1) * (n-1) = 162.
    # Aceitamos uma margem para esquemas alternativos de invocação.
    assert contador["comparacoes"] < 50  # Muito abaixo do não otimizado.
    
class TestEquivalencia:
  """Os três algoritmos devem produzir o mesmo resultado."""
  @pytest.mark.parametrize(
    "entrada",
    [
      [],
      [1],
      [3, 1, 2],
      [5, 2, 8, 1, 9, 3, 7, 4, 6],
      [1, 1, 1],
      [9, 7, 5, 3, 1],
    ],
  )
  def test_resultados_coincidem(self, entrada):
    ll = _lista(*entrada)
    r_bubble = list(bubble_sort(ll))
    r_insertion = list(insertion_sort(ll))
    r_selection = list(selection_sort(ll))
    assert r_bubble == r_insertion == r_selection == sorted(entrada)