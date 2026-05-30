# benchmark dos algoritmos de ordenação
# mede impiricamente o tempo de execução dos algoritmos de ordenação
# apresenta os resultados em tabela e gráfico
# valida impiricamente a complexidade teórica dos algoritmos
# execução: python -m src.algoritmos.benchmark

from __future__ import annotations
 
import random
import statistics
import time
from dataclasses import dataclass
from typing import Callable
 
from src.algoritmos.ordenacao import (
    bubble_sort,
    insertion_sort,
    selection_sort,
)
from src.estruturas.lista_ligada import ListaLigada
 
# Tipo do algoritmo: recebe ListaLigada, devolve ListaLigada ordenada.
Algoritmo = Callable[[ListaLigada[int]], ListaLigada[int]]
 
ALGORITMOS: list[tuple[str, Algoritmo]] = [
    ("Bubble Sort", bubble_sort),
    ("Insertion Sort", insertion_sort),
    ("Selection Sort", selection_sort),
]
 
TAMANHOS_DEFAULT: list[int] = [50, 100, 250, 500, 1000, 2000]
REPETICOES_DEFAULT: int = 5
SEMENTE_DEFAULT: int = 42
 
 
@dataclass(frozen=True)
class Medicao:
  """Resultado de uma medição: tempo médio e desvio padrão (segundos)."""
  media: float
  desvio: float

def _gerar_aleatorio(n: int, rng: random.Random) -> ListaLigada[int]:
  """Gera uma ListaLigada com n inteiros aleatoriamente ordenados."""
  valores = list(range(n))
  rng.shuffle(valores)
  lista: ListaLigada[int] = ListaLigada()
  for v in valores:
    lista.inserir_fim(v)
  return lista
 
def _gerar_ordenado(n: int) -> ListaLigada[int]:
  """Gera uma ListaLigada com n inteiros já ordenados."""
  lista: ListaLigada[int] = ListaLigada()
  for v in range(n):
    lista.inserir_fim(v)
  return lista
 
def _gerar_inverso(n: int) -> ListaLigada[int]:
  """Gera uma ListaLigada com n inteiros em ordem decrescente."""
  lista: ListaLigada[int] = ListaLigada()
  for v in range(n, 0, -1):
    lista.inserir_fim(v)
  return lista

def _medir(
    algoritmo: Algoritmo,
    construtor: Callable[[], ListaLigada[int]],
    repeticoes: int,
) -> Medicao:
  """
  Mede o tempo de execução de algoritmo sobre entradas construídas
  por construtor. Realiza repeticoes medições independentes e
  devolve a média e o desvio padrão.

  O construtor é invocado antes de cada repetição para garantir que o
  algoritmo recebe sempre uma entrada nas mesmas condições (sem
  interferência de uma execução prévia que pudesse, por exemplo, ter
  aquecido a cache da CPU).
  """
  tempos: list[float] = []
  for _ in range(repeticoes):
    entrada = construtor()
    inicio = time.perf_counter()
    _ = algoritmo(entrada)
    fim = time.perf_counter()
    tempos.append(fim - inicio)
  media = statistics.fmean(tempos)
  desvio = statistics.stdev(tempos) if len(tempos) > 1 else 0.0
  return Medicao(media=media, desvio=desvio)

def executar_benchmark(
    tamanhos: list[int] | None = None,
    repeticoes: int = REPETICOES_DEFAULT,
    semente: int = SEMENTE_DEFAULT,
) -> dict[str, dict[str, list[Medicao]]]:
  """
  Executa o benchmark completo e devolve os resultados estruturados:

      resultados[cenario][algoritmo] = [Medicao, ...]

  onde cada lista tem o mesmo comprimento de `tamanhos`.
  """
  if tamanhos is None:
    tamanhos = TAMANHOS_DEFAULT
  rng = random.Random(semente)

  cenarios: dict[str, Callable[[int], ListaLigada[int]]] = {
    "Aleatório": lambda n: _gerar_aleatorio(n, rng),
    "Já ordenado": _gerar_ordenado,
    "Ordem inversa": _gerar_inverso,
  }

  resultados: dict[str, dict[str, list[Medicao]]] = {
    nome: {alg_nome: [] for alg_nome, _ in ALGORITMOS}
    for nome in cenarios
  }

  for nome_cenario, gerador in cenarios.items():
    for n in tamanhos:
      for nome_alg, alg in ALGORITMOS:
        medicao = _medir(alg, lambda n=n, g=gerador: g(n), repeticoes)
        resultados[nome_cenario][nome_alg].append(medicao)

  return resultados

def imprimir_tabela(
  resultados: dict[str, dict[str, list[Medicao]]],
  tamanhos: list[int],
) -> None:
  """
  Imprime os resultados em tabelas formatadas, uma por cenário.
  """
  for cenario, por_alg in resultados.items():
    print(f"\nCenário: {cenario}")
    cab = f"  {'n':>6}  " + "  ".join(f"{a:>18}" for a in por_alg.keys())
    print(cab)
    print("  " + "-" * (len(cab) - 2))
    for i, n in enumerate(tamanhos):
      celulas = []
      for nome_alg, medicoes in por_alg.items():
        m = medicoes[i]
        celulas.append(f"{m.media * 1000:8.2f} ± {m.desvio * 1000:5.2f} ms")
      print(f"  {n:>6}  " + "  ".join(celulas))
 
def gerar_grafico(
  resultados: dict[str, dict[str, list[Medicao]]],
  tamanhos: list[int],
  caminho_saida: str,
) -> None:
  """
  Gera um gráfico com três subgráficos (um por cenário), comparando
  os três algoritmos. Guarda em `caminho_saida`.

  A importação de `matplotlib` é feita aqui, dentro da função, para
  que o módulo possa ser usado para medição mesmo em ambientes sem
  matplotlib instalado.
  """
  import matplotlib.pyplot as plt  # importação local; ver docstring

  cenarios = list(resultados.keys())
  fig, axes = plt.subplots(1, len(cenarios), figsize=(15, 4.5), sharey=False)
  if len(cenarios) == 1:
    axes = [axes]

  cores = {
    "Bubble Sort": "#1f77b4",
    "Insertion Sort": "#ff7f0e",
    "Selection Sort": "#2ca02c",
  }

  for ax, cenario in zip(axes, cenarios):
    for nome_alg, medicoes in resultados[cenario].items():
      medias = [m.media * 1000 for m in medicoes]  # em ms
      ax.plot(
        tamanhos,
        medias,
        marker="o",
        label=nome_alg,
        color=cores.get(nome_alg, None),
      )
    ax.set_title(cenario)
    ax.set_xlabel("Tamanho da entrada (n)")
    ax.set_ylabel("Tempo (ms)")
    ax.grid(True, alpha=0.3)
    ax.legend()

  fig.suptitle("Comparação empírica dos algoritmos de ordenação", fontsize=13)
  fig.tight_layout()
  fig.savefig(caminho_saida, dpi=120, bbox_inches="tight")
  plt.close(fig)
 
 
def main() -> None:
  """Executa o benchmark completo e produz tabela + gráfico."""
  import os

  tamanhos = TAMANHOS_DEFAULT
  print("A executar benchmark...")
  print(f"  Tamanhos    : {tamanhos}")
  print(f"  Repetições  : {REPETICOES_DEFAULT} por medição")
  print(f"  Semente RNG : {SEMENTE_DEFAULT}")

  resultados = executar_benchmark(
    tamanhos=tamanhos,
    repeticoes=REPETICOES_DEFAULT,
    semente=SEMENTE_DEFAULT,
  )

  imprimir_tabela(resultados, tamanhos)

  caminho = os.path.join("relatorio", "imagens", "benchmark_ordenacao.png")
  os.makedirs(os.path.dirname(caminho), exist_ok=True)
  gerar_grafico(resultados, tamanhos, caminho)
  print(f"\nGráfico guardado em: {caminho}")
 
 
if __name__ == "__main__":
  main()