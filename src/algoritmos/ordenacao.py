"""
Algoritmos de ordenação.

Estes algoritmos operam sobre a lista ligada utilizando um arry auxiliar
os algoritmos recebem uma lista e retornam uma nova lista ordenada
sem modificar evita side effects.

cada função recebe:
- lista: ListaLigada[T] para ser ordenada
- chave: função callable[[T], Any] muito especifico do python 
- reverso: se true ordena na ordem decrescente, se false ordena na ordem crescente

Complexidades (n = nº de elementos)
-----------------------------------
- Bubble Sort   : melhor O(n), médio/pior O(n²); estável.
- Insertion Sort: melhor O(n), médio/pior O(n²); estável.
- Selection Sort: melhor/médio/pior O(n²); não estável.


vamos utilizar um array auxiliar 
porque a manipulação direta de nós de uma lista ligada simples para fins de
ordenação introduz duas distorções: (i) o acesso por índice torna-se
O(n), elevando o Bubble Sort ingénuo a O(n³); (ii) o Selection Sort em
lista ligada exige percorrer a lista para encontrar o mínimo e percorrê
-la de novo para o extrair, o que dificulta a comparação justa com os
restantes algoritmos. Copiar para um array contíguo (tipo `list` nativo
do Python) restitui o comportamento canónico O(n²) descrito na
literatura e permite ao módulo de benchmark produzir medições fiéis às
complexidades teóricas. O `list` é aqui usado estritamente como buffer
de trabalho, não como substituto das estruturas de dados do projeto.
"""

from __future__ import annotations
 
from typing import Any, Callable, TypeVar
 
from src.estruturas.lista_ligada import ListaLigada
 
T = TypeVar("T")

def _identidade(valor: T) -> T:
  return valor

def _copiar_para_array(lista: ListaLigada[T]) -> list[T]:
  # copia de elementos O(n)
  new_array: list[T] = []
  for elemento in lista:
    new_array.append(elemento)
  return new_array

def _array_para_lista(array: list[T]) -> ListaLigada[T]:
  # gera uma nova lista ligada a partir de um array O(n)
  # utiliza inserção no fim para manter a ordem O(1)
  nova_lista: ListaLigada[T] = ListaLigada()
  for elemento in array:
    nova_lista.inserir_fim(elemento)
  return nova_lista

def _comparar(a: Any, b: Any, reverso: bool) -> bool:
  # devolve true de a deve vir antes de b na ordenacao
  # a < b se reverso for false, a > b se reverso for true
  if reverso:
    return a > b
  else:
    return a < b
  
  
# 1º algoritmo: Bubble Sort
def bubble_sort(
  lista: ListaLigada[T],
  chave: Callable[[T], Any] = _identidade,
  reverso: bool = False
  ) -> ListaLigada[T]:
  # percorre repetidamente o array, trocando os elementos adjacentes que estejam 
  # fora de ordem, inclue otimização para um saida antecipada
  # se nao existirem trocas, a lista já está ordenada 
  # Complexidade: melhor O(n), médio/pior O(n²). Estável.
  array = _copiar_para_array(lista) # O(n)
  tamanho = len(array)
  for i in range(tamanho -1):
    houve_troca = False
    for j in range(tamanho -1 -i):
      if _comparar(chave(array[j+1]), chave(array[j]), reverso):
        array[j], array[j+1] = array[j+1], array[j]
        houve_troca = True
    if not houve_troca:
      break
  return _array_para_lista(array)

# 2º algoritmo: Insertion Sort
def insertion_sort(
  lista: ListaLigada[T],
  chave: Callable[[T], Any] = _identidade,
  reverso: bool = False
  ) -> ListaLigada[T]:
  # mantem os menores numeros a esquerda e desloca os maiores para a direita
  # Complexidade: melhor O(n) (entrada ordenada), médio/pior O(n²). Estável.
  array = _copiar_para_array(lista)
  tamanho = len(array)
  for i in range(1, tamanho):
    valor_atual = array[i]
    chave_atual = chave(valor_atual)
    j = i - 1
    # desloca os elementos maiores para a direita
    while j >= 0 and _comparar(chave_atual, chave(array[j]), reverso):
      array[j + 1] = array[j]
      j -= 1
    array[j + 1] = valor_atual
  return _array_para_lista(array)

# 3º algoritmo: Selection Sort
def selection_sort(
  lista: ListaLigada[T],
  chave: Callable[[T], Any] = _identidade,
  reverso: bool = False,
) -> ListaLigada[T]:
  """
  Em cada iteração, localiza o menor (ou maior, se reverso) elemento
  do sub-array não ordenado e coloca-o na posição correta, trocando-o
  com o elemento da fronteira.

  Complexidade: melhor/médio/pior O(n²). NÃO estável
  """
  array = _copiar_para_array(lista)
  tamanho = len(array)

  for i in range(tamanho - 1):
    # Localiza o índice do "menor" elemento entre i..tamanho-1, onde
    # "menor" depende de `reverso`.
    indice_extremo = i
    chave_extrema = chave(array[i])
    for j in range(i + 1, tamanho):
      chave_j = chave(array[j])
      if _comparar(chave_j, chave_extrema, reverso):
        indice_extremo = j
        chave_extrema = chave_j
    if indice_extremo != i:
      array[i], array[indice_extremo] = array[indice_extremo], array[i]

  return _array_para_lista(array)