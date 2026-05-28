# entidade autocarro
# passageiros abordo sao geridos por uma lista ligada
# autocarro tem capacidade maxima de passageiros e mantem referencia para a paragem onde se encontra

from typing import Optional
 
from .paragem import Paragem
from .passageiro import Passageiro
from src.estruturas.lista_ligada import ListaLigada


class AutocarroCheioError(Exception):
  # lançada ao tentar embarcar um passageiro com a lotação esgotada
  pass
 
 
class AutocarroVazioError(Exception):
  # lançada ao tentar desembarcar de um autocarro sem passageiros
  pass

class Autocarro:
  # Autocarro com capacidade limitada e posição na linha
  
  __slots__ = ("_capacidade", "_passageiros", "_posicao_atual")
  
  def __init__(self, capacidade: int) -> None:
    if capacidade <= 0:
      raise ValueError("A capacidade do autocarro deve ser positiva.")
    self._capacidade: int = capacidade
    self._passageiros: ListaLigada[Passageiro] = ListaLigada()
    self._posicao_atual: Optional[Paragem] = None
    
  @property
  def capacidade(self) -> int:
      # Lotação máxima do autocarro
      return self._capacidade
 
  @property
  def posicao_atual(self) -> Optional[Paragem]:
    return self._posicao_atual
  
  def lotacao(self) -> int:
      return self._passageiros.tamanho()
 
  def lugares_livres(self) -> int:
    return self._capacidade - self._passageiros.tamanho()

  def esta_cheio(self) -> bool:
    return self.lugares_livres() == 0

  def esta_vazio(self) -> bool:
    return self._passageiros.esta_vazia()

  def passageiros_a_bordo(self) -> ListaLigada[Passageiro]:
    # Devolve uma cópia dos passageiros a bordo, pela
    # ordem de entrada. alterar não afeta o autocarro. O(n).
    copia: ListaLigada[Passageiro] = ListaLigada()
    for passageiro in self._passageiros:
      copia.inserir_fim(passageiro)
    return copia
  
  # entrada
  def embarcar(self, passageiro: Passageiro) -> None:
    # Faz entrar um passageiro no autocarro se houver lugares livres. O(1).
    if self.esta_cheio():
      raise AutocarroCheioError(
        f"Lotação esgotada (capacidade {self._capacidade})."
      )
    self._passageiros.inserir_fim(passageiro)
    
  # saída
  def desembarcar_passageiro(self) -> Passageiro:
    # Faz descer o passageiro que entrou primeiro (ordem FIFO). O(1)
    if self._passageiros.esta_vazia():
      raise AutocarroVazioError("Não há passageiros a bordo para desembarcar.")
    return self._passageiros.remover_posicao(0)
 
  def desembarcar_todos(self) -> ListaLigada[Passageiro]:
    # Faz descer todos os passageiros, devolvendo-os numa lista ligada pela ordem de entrada. O(n)
    descidos: ListaLigada[Passageiro] = ListaLigada()
    while not self._passageiros.esta_vazia():
      descidos.inserir_fim(self._passageiros.remover_posicao(0))
    return descidos
  
  # movimento
  def mover_para(self, paragem: Paragem) -> None:
    # Move o autocarro para a paragem indicada. O(1)
    # quem decide qual é a próxima paragem é o controlador da linha, não o autocarro
    self._posicao_atual = paragem

  def __repr__(self) -> str:
    local = self._posicao_atual.nome if self._posicao_atual else "—"
    return (
      f"Autocarro(lotação={self.lotacao()}/{self._capacidade}, "
      f"posição={local!r})"
    )