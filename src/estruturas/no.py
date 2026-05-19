from __future__ import annotations
from typing import Generic, TypeVar, Optional

# Definir um tipo genérico para os dados armazenados no nó
T = TypeVar('T')

class No(Generic[T]):
  """
  Atributos
  ---------
  valor : T
      Conteúdo armazenado pelo nó. Pode ser qualquer tipo de dado (Paragem, Passageiro, str, etc.).
  proximo : No[T] | None
      Referência para o próximo nó na lista. Pode ser None se este for o último nó.
  """
  
  __slots__ = ("valor", "proximo")
  
  def __init__(self, valor: T, proximo: Optional["No[T]"] = None) -> None:
    self.valor: T = valor
    self.proximo: Optional["No[T]"] = proximo
    
  def __repr__(self) -> str:
    # Representação útil para depuração; não inclui o nó seguinte
    # para evitar recursão infinita em listas longas.
    return f"No(valor={self.valor})"