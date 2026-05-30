# motor de simulação do movimento do autocarro ao longo da linha
# operações:
# 1. move o autocarro para a próxima paragem
# 2. embarca os passageiros que estão à espera na paragem
# 3. desembarca os passageiros que chegaram ao destino
# cada operação produz um ou mais EventoSimulacao que representa
# um registo estruturado do que aconteceu
# Esta separação entre o motor (que produz eventos) e a apresentação
# (que os formata) é deliberada: garante baixo acoplamento e permite
#substituir a interface (CLI, gráfica, ficheiro de log) sem alterar a
#lógica de simulação.

from __future__ import annotations
 
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
 
from src.dominio.autocarro import Autocarro, AutocarroCheioError
from src.dominio.linha import Linha
from src.dominio.paragem import Paragem
from src.dominio.passageiro import Passageiro
from src.estruturas.lista_ligada import ListaLigada
 
 
class FimDaLinhaError(Exception):
  """lancada ao tentar avançar para além da última paragem da linha."""
 
 
class LinhaVaziaError(Exception):
  """lancada ao tentar simular numa linha sem paragens."""
 
 
class TipoEvento(Enum):
  """Tipos de eventos produzidos pelo simulador."""
  CHEGADA = auto()
  DESEMBARQUE = auto()
  EMBARQUE = auto()
  NAO_HA_QUEM_DESEMBARCAR = auto()
  NAO_HA_QUEM_EMBARCAR = auto()
  AUTOCARRO_CHEIO = auto()
  
@dataclass(frozen=True)
class EventoSimulacao:
  tipo: TipoEvento
  paragem: str
  passageiro: Optional[str] = None
  detalhe: str = ""
  
class Simulador:
 
  __slots__ = ("_linha", "_autocarro", "_indice_proxima_paragem")

  def __init__(self, linha: Linha, autocarro: Autocarro) -> None:
    self._linha: Linha = linha
    self._autocarro: Autocarro = autocarro
    # Índice (0-based) da próxima paragem a visitar na ListaLigada
    # da Linha. Começa em 0 (ainda não saiu); após o primeiro avanço
    # passa a 1 (já está na paragem 0 e a próxima é a 1).
    self._indice_proxima_paragem: int = 0
 
  @property
  def linha(self) -> Linha:
    return self._linha
 
  @property
  def autocarro(self) -> Autocarro:
    return self._autocarro
 
  def terminou(self) -> bool:
    """Indica se o autocarro já passou pela última paragem da linha."""
    return self._indice_proxima_paragem >= self._linha.numero_paragens

  def avancar_uma_paragem(
    self,
    embarcar_um: bool = True,
    desembarcar_um: bool = True,
  ) -> ListaLigada[EventoSimulacao]:
    
    if self._linha.esta_vazia():
      raise LinhaVaziaError("A linha não tem paragens; nada a simular.")
    if self.terminou():
      raise FimDaLinhaError("O autocarro já percorreu toda a linha.")

    eventos: ListaLigada[EventoSimulacao] = ListaLigada()

    # 1. Mover o autocarro para a próxima paragem.
    # Iteração direta para obter a paragem no índice pretendido,
    # evitando O(n) por construção repetida da lista completa.
    proxima: Optional[Paragem] = None
    for i, paragem in enumerate(self._linha.listar_percurso()):
      if i == self._indice_proxima_paragem:
        proxima = paragem
        break
    assert proxima is not None  # garantido pelas verificações iniciais
    self._autocarro.mover_para(proxima)
    self._indice_proxima_paragem += 1

    eventos.inserir_fim(
      EventoSimulacao(
        tipo=TipoEvento.CHEGADA,
        paragem=proxima.nome,
        detalhe=(
          f"a bordo: {self._autocarro.lotacao()}/"
          f"{self._autocarro.capacidade}; "
          f"em espera: {proxima.numero_em_espera()}"
        ),
      )
    )

    # 2. Desembarque.
    if desembarcar_um:
        eventos.inserir_fim(self._desembarcar(proxima))

    # 3. Embarque.
    if embarcar_um:
        eventos.inserir_fim(self._embarcar(proxima))

    return eventos

  def simular_percurso_completo(self) -> ListaLigada[EventoSimulacao]:
      todos: ListaLigada[EventoSimulacao] = ListaLigada()
      while not self.terminou():
        for evento in self.avancar_uma_paragem():
          todos.inserir_fim(evento)
      return todos

  def _desembarcar(self, paragem: Paragem) -> EventoSimulacao:
    if self._autocarro.esta_vazio():
      return EventoSimulacao(
        tipo=TipoEvento.NAO_HA_QUEM_DESEMBARCAR,
        paragem=paragem.nome,
      )
    passageiro: Passageiro = self._autocarro.desembarcar_passageiro()
    return EventoSimulacao(
      tipo=TipoEvento.DESEMBARQUE,
      paragem=paragem.nome,
      passageiro=passageiro.nome,
      detalhe=f"a bordo agora: {self._autocarro.lotacao()}",
    )

  def _embarcar(self, paragem: Paragem) -> EventoSimulacao:
    if not paragem.tem_passageiros():
      return EventoSimulacao(
        tipo=TipoEvento.NAO_HA_QUEM_EMBARCAR,
        paragem=paragem.nome,
      )
    if self._autocarro.esta_cheio():
      return EventoSimulacao(
        tipo=TipoEvento.AUTOCARRO_CHEIO,
        paragem=paragem.nome,
        detalhe=(
          f"em espera: {paragem.numero_em_espera()} "
          f"(não pôde embarcar)"
        ),
      )
    # Caso geral: há quem espere e há lugar.
    passageiro: Passageiro = paragem.embarcar_passageiro()
    try:
      self._autocarro.embarcar(passageiro)
    except AutocarroCheioError:
      paragem.adicionar_passageiro(passageiro)
      return EventoSimulacao(
        tipo=TipoEvento.AUTOCARRO_CHEIO,
        paragem=paragem.nome,
        passageiro=passageiro.nome,
      )
    return EventoSimulacao(
      tipo=TipoEvento.EMBARQUE,
      paragem=paragem.nome,
      passageiro=passageiro.nome,
      detalhe=f"a bordo agora: {self._autocarro.lotacao()}",
    )