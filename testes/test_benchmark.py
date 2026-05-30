#  pytest testes/test_benchmark.py -v

import random
 
import pytest
 
from src.algoritmos.benchmark import (
  ALGORITMOS,
  Medicao,
  _gerar_aleatorio,
  _gerar_inverso,
  _gerar_ordenado,
  executar_benchmark,
)
 
class TestGeradores:
  def test_aleatorio_tem_tamanho_correto(self):
    rng = random.Random(0)
    ll = _gerar_aleatorio(50, rng)
    assert ll.tamanho == 50

  def test_aleatorio_contem_todos_os_valores(self):
    # Deve ser uma permutação de 0..n-1.
    rng = random.Random(0)
    ll = _gerar_aleatorio(50, rng)
    assert sorted(list(ll)) == list(range(50))

  def test_ordenado_esta_crescente(self):
    ll = _gerar_ordenado(20)
    valores = list(ll)
    assert valores == sorted(valores)
    assert valores == list(range(20))

  def test_inverso_esta_decrescente(self):
    ll = _gerar_inverso(20)
    valores = list(ll)
    assert valores == sorted(valores, reverse=True)
 
 
class TestExecutarBenchmark:
  def test_estrutura_dos_resultados(self):
    # Usar tamanhos muito pequenos para o teste correr depressa.
    tamanhos = [10, 20]
    resultados = executar_benchmark(
      tamanhos=tamanhos, repeticoes=2, semente=0
    )

    # Há três cenários esperados.
    assert set(resultados.keys()) == {"Aleatório", "Já ordenado", "Ordem inversa"}

    nomes_alg = {nome for nome, _ in ALGORITMOS}
    for cenario, por_alg in resultados.items():
      # Cada cenário tem os três algoritmos.
      assert set(por_alg.keys()) == nomes_alg
      for alg, medicoes in por_alg.items():
        # Uma medição por tamanho.
        assert len(medicoes) == len(tamanhos)
        for m in medicoes:
          assert isinstance(m, Medicao)
          assert m.media >= 0
          assert m.desvio >= 0

  def test_resultados_sao_reproduzivel_com_a_mesma_semente(self):
    # Comparar conteúdos das entradas, não tempos.
    # Para isso, basta verificar que a geração aleatória repetida
    # com a mesma semente produz a mesma permutação.
    a = _gerar_aleatorio(30, random.Random(123))
    b = _gerar_aleatorio(30, random.Random(123))
    assert list(a) == list(b)