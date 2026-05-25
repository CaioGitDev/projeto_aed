"""
Fila genérica com disciplina FIFO (First-In, First-Out).
  
A reutilização da classe No
 
Complexidades
-------------
- enfileirar   : O(1)
- desenfileirar: O(1)
- frente       : O(1)
- tamanho      : O(1)  (mantido em cache)
- esta_vazia   : O(1)
- listar       : O(n)
"""


from __future__ import annotations
from typing import Generic, Iterator, Optional, TypeVar
from .lista_ligada import ListaLigada
from .no import No

T = TypeVar('T')

class FilaVaziaError(Exception):
  """Exceção lançada ao tentar acessar elementos de uma fila vazia."""
  
class Fila(Generic[T]):
  # Fila FIFO, pensado para funcionar exatamente como uma fila para o autocarro, 
  # quem chega primeiro, sai primeiro.
  
  __slots__ = ("_frente", "_tras", "_tamanho")
  
  def __init__(self) -> None:
    self._frente: Optional[No[T]] = None
    self._tras: Optional[No[T]] = None
    self._tamanho: int = 0
    
  # CONSULTAS
  @property
  def tamanho(self) -> int:
    # numero de elementos em fila O(1)
    return self._tamanho
  
  def esta_vazia(self) -> bool:
    # Verifica se a fila está vazia O(1)
    return self._tamanho == 0
  
  def frente(self) -> T:
    # retorna o elemento na frente da fila sem remover O(1)
    # Lança FilaVaziaError se a fila estiver vazia.
    if self._frente is None:
      raise FilaVaziaError("A fila está vazia.")
    return self._frente.valor
  
  
  # Operações
  def enfileirar(self, valor: T) -> None:
    # Adiciona um elemento ao final da fila O(1)
    novo_no = No(valor)
    if self._tras is None:
      # fila esta vazia, novo nó é frente e tras
      self._frente = novo_no
      self._tras = novo_no
    else:
      self._tras.proximo = novo_no
      self._tras = novo_no
    self._tamanho += 1
  
  def desenfileirar(self) -> T:
    # remove e retorna o elemento na frente da fila O(1)
    # Lança FilaVaziaError se a fila estiver vazia.
    if self._frente is None:
      raise FilaVaziaError("A fila está vazia.")
    
    no_removido = self._frente
    self._frente = no_removido.proximo
    
    if self._frente is None:
      # fila ficou vazia, atualizar o valor de tras
      self._tras = None
    self._tamanho -= 1
    return no_removido.valor
  
  
  # Listar
  def listar(self) -> ListaLigada[T]:
    # Retorna uma lista ligada com os elementos da fila na ordem correta O(n)
    # consultar pessoas em fila O(n)
    lista: ListaLigada[T] = ListaLigada()
    atual = self._frente
    while atual is not None:
      lista.inserir_fim(atual.valor)
      atual = atual.proximo
    return lista
  
  # Auxiliares
  def __len__(self) -> int:
    return self._tamanho
 
  def __iter__(self) -> Iterator[T]:
    # Itera sobre os elementos da fila, da frente para trás, sem os remover. O(n)
    atual = self._frente
    while atual is not None:
        yield atual.valor
        atual = atual.proximo

  def __repr__(self) -> str:
    valores = ", ".join(repr(v) for v in self)
    return f"Fila(frente=[{valores}]=trás)"