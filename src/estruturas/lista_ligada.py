"""
Lista ligada simples.

Complexidades
-------------
- inserir_inicio  : O(1)
- inserir_fim     : O(1)
- inserir_posicao : O(n) 
- remover_valor   : O(n)
- remover_posicao : O(n)
- obter           : O(n)
- tamanho         : O(1)
- esta_vazia      : O(1)
- iteração        : O(n)
"""

from __future__ import annotations
from typing import Generic, Iterator, Optional, TypeVar
from .no import No

# Definir um tipo genérico para os dados armazenados na lista
T = TypeVar('T')

class ListaLigada(Generic[T]):
  __slots__ = ("_cabeca", "_cauda", "_tamanho")
  
  def __init__(self) -> None:
    self._cabeca: Optional[No[T]] = None
    self._cauda: Optional[No[T]] = None
    self._tamanho: int = 0
    
  # GETS
  @property
  def tamanho(self) -> int:
    return self._tamanho
  
  def esta_vazia(self) -> bool:
    return self._tamanho == 0
  
  def obter(self, posicao: int) -> T:
    self._validar_posicao_existente(posicao) # O(1)
    no = self.no_em_posicao(posicao) # O(n)
    return no.valor
  
  # INSERÇÕES
  def inserir_inicio(self, valor: T) -> None:
    novo_no = No(valor, proximo=self._cabeca)
    self._cabeca = novo_no
    if self._cauda is None:
      # se a lista estiver vazia, a cauda também deve apontar para o novo nó
      self._cauda = novo_no
    self._tamanho += 1
    
  def inserir_fim(self, valor: T) -> None:
    novo_no = No(valor)
    if self._cauda is None:
      # se lista vazia: cabeça = cauda
      self._cabeca = novo_no
      self._cauda = novo_no
    else:
      # se lista não estiver vazia: cauda.proximo = novo_no, cauda = novo_no
      self._cauda.proximo = novo_no
      self._cauda = novo_no
    self._tamanho += 1
    
  def inserir_posicao(self, valor: T, posicao: int) -> None:
    # Insere um elemento na posição indicada, com proteção outof bounds.
    if posicao < 0 or posicao > self._tamanho:
      raise IndexError(f"Posição inválida: {posicao}. Deve ser entre 0 e {self._tamanho}.")
    
    if posicao == 0:
      self.inserir_inicio(valor)
      return
    
    if posicao == self._tamanho:
      self.inserir_fim(valor)
      return
    
    # Inserção no meio da lista
    no_anterior = self.no_em_posicao(posicao - 1) # O(n)
    novo_no = No(valor, proximo=no_anterior.proximo)
    no_anterior.proximo = novo_no
    self._tamanho += 1
    
  # REMOÇÕES
  def remover_posicao(self, posicao: int) -> T:
    self._validar_posicao_existente(posicao) # O(1)
    
    if posicao == 0:
      assert self._cabeca is not None  # Garantir que a cabeça não é None
      valor_removido = self._cabeca
      self._cabeca = valor_removido.proximo
      if self._cabeca is None:
        # Se a lista ficou vazia, atualizar a cauda também
        self._cauda = None
      self._tamanho -= 1
      return valor_removido.valor
    
    no_anterior = self.no_em_posicao(posicao - 1) # O(n)
    assert no_anterior.proximo is not None  # Garantir que o próximo nó existe
    valor_removido = no_anterior.proximo
    if valor_removido is self._cauda:
      # Se o nó removido é a cauda, atualizar a cauda para o nó anterior
      self._cauda = no_anterior
    self._tamanho -= 1
    return valor_removido.valor
  
  def remover_valor(self, valor: T) -> None:
    # Remove a primeira ocorrencia do vaor indicado, se nao existir lança ValueError.
    no_anterior: Optional[No[T]] = None
    no_atual: Optional[No[T]] = self._cabeca
    
    while no_atual is not None:
      if no_atual.valor == valor:
        if no_anterior is None:
          # remover a cabeça
          self._cabeca = no_atual.proximo
        else:
          no_anterior.proximo = no_atual.proximo
        
        if no_atual is self._cauda:
          # se o nó removido for a cauda, atualizar a cauda para o nó anterior
          self._cauda = no_anterior
        
        self._tamanho -= 1
        return
      
      no_anterior = no_atual
      no_atual = no_atual.proximo
    
    raise ValueError(f"Valor {valor} não encontrado na lista.")
  
  
  # AUXILIARES e ITERAÇÃO
  def __iter__(self) -> Iterator[T]:
    # Iteração simples sobre os valores da lista, do início ao fim. O(n)
    no_atual = self._cabeca
    while no_atual is not None:
      yield no_atual.valor
      no_atual = no_atual.proximo
  
  def __len__(self) -> int:
    # Permite usar len(lista) para obter o tamanho da lista. O(1)
    return self._tamanho
  
  def __contains__(self, valor:object) -> bool:
    # Permite usar "valor in lista" para verificar se um valor está presente na lista. O(n)
    for elemento in self:
      if elemento == valor:
        return True
    return False
  
  def __eq__(self, outro: object) -> bool:
    # Permite comparar duas listas utilizando == para verificar se tem os mesmos elementos na mesma ordem. O(n)
    if not isinstance(outro, ListaLigada):
      return NotImplemented
    
    if self._tamanho != outro._tamanho:
      return False
    
    no_atual_self = self._cabeca
    no_atual_outro = outro._cabeca
  
    while no_atual_self is not None and no_atual_outro is not None:
      if no_atual_self.valor != no_atual_outro.valor:
        return False
      no_atual_self = no_atual_self.proximo
      no_atual_outro = no_atual_outro.proximo
  
    return True
  
  def __repr__(self):
    # Representação útil para depuração; mostra os valores da lista.
    valores = ", ".join(repr(v) for v in self)
    return f"ListaLigada([{valores}])"
  
  # METODOS INTERNOS
  def _validar_posicao_existente(self, posicao: int) -> None:
    # Valida se a posição é válida para acesso ou remoção (entre 0 e tamanho-1). O(1)
    if posicao < 0 or posicao >= self._tamanho:
      raise IndexError(
          f"Posição {posicao} fora dos limites [0, {self._tamanho - 1}]."
      )
      
  def no_em_posicao(self, posicao: int) -> No[T]:
    # Retorna o nó na posição indicada. Assumindo que a posição é válida. O(n)
    no_atual = self._cabeca
    for _ in range(posicao):
      assert no_atual is not None  
      no_atual = no_atual.proximo
    assert no_atual is not None  
    return no_atual