# Entidade Paragem
# Representa uma paragem de autocarro, com um nome e uma lista de passageiros
# Em espera atraves de uma fila (FIFO)

from __future__ import annotations

from .passageiro import Passageiro
from ..estruturas.fila import Fila, FilaVaziaError
from ..estruturas.lista_ligada import ListaLigada

class ParagemVaziaError(Exception):
  # Lançada ao tentar adicionar um passageiro de uma paragem sem fila
  pass
  
  
class Paragem:
  # Paragem da linha, com nome e fila de passageiros
  
  __slots__ = ("_nome", "_fila")
  
  def __init__(self, nome: str) -> None:
    if not nome or not nome.strip():
      raise ValueError("O nome da paragem não pode ser vazio.")
    
    self._nome: str = nome.strip()
    self._fila: Fila[Passageiro] = Fila()
    
  @property
  def nome(self) -> str:
    return self._nome
  
  # Gestão de passageiros 
  def adicionar_passageiro(self, passageiro: Passageiro) -> None:
    # adiciona um passageiro à fila da paragem O(1)
    self._fila.enfileirar(passageiro)
    
  def embarcar_passageiro(self) -> Passageiro:
    # remove e retorna o passageiro na frente da fila O(1)
    # se a fila estiver vazia, lança ParagemVaziaError
    try:
      return self._fila.desenfileirar()
    except FilaVaziaError as exc:
      raise ParagemVaziaError(
        f"A paragem {self._nome!r} não tem passageiros em espera."
      ) from exc
      
  def numero_em_espera(self) -> int:
    # retorna o número de passageiros em espera na fila O(1)
    return self._fila.tamanho
  
  def passageiros_em_espera(self) -> ListaLigada[Passageiro]:
    # retorna uma lista ligada com os passageiros em espera, na ordem da fila O(n)
    return self._fila.listar()
  
  def tem_passageiros(self) -> bool:
    # Indica se há passageiros em espera na paragem O(1)
    return not self._fila.esta_vazia()
  
  # Representação e comparação
  def __eq__(self, outro: object) -> bool:
    if not isinstance(outro, Paragem):
      return NotImplemented
    return self._nome == outro._nome

  def __hash__(self) -> int:
    return hash(self._nome)

  def __repr__(self) -> str:
    return f"Paragem(nome={self._nome!r}, em_espera={self.numero_em_espera()})"