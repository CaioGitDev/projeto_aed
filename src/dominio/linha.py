# entidade linha

# representa uma linha de autocarro com uma sequencia ordenada de paragens
# a linha pode sob medida construir um grafo que reflete a topologia da linha
 
from __future__ import annotations
 
from .paragem import Paragem
from src.estruturas.grafo import Grafo
from src.estruturas.lista_ligada import ListaLigada

from src.dominio import paragem



class ParagemDuplicadaError(Exception):
  # lançada ao inserir uma paragem com nome já existente na linha.
  pass
 
 
class ParagemNaoEncontradaError(Exception):
  # lançada ao referenciar uma paragem inexistente na linha.
  pass

class Linha:
  # linha squencia ordenada de paragens
  
  __slots__ = ("_nome", "_paragens")
  
  def __init__(self, nome: str) -> None:
    if not nome or not nome.strip():
      raise ValueError("O nome da linha não pode ser vazio.")
    self._nome: str = nome.strip()
    self._paragens: ListaLigada[Paragem] = ListaLigada()
    
  # consultas
  @property
  def nome(self) -> str:
      return self._nome

  @property
  def numero_paragens(self) -> int:
    return self._paragens.tamanho

  def esta_vazia(self) -> bool:
    return self._paragens.esta_vazia()

  def contem_paragem(self, nome: str) -> bool:
    return self._localizar(nome) is not None

  def obter_paragem(self, nome: str) -> Paragem:
    paragem = self._localizar(nome)
    if paragem is None:
      raise ParagemNaoEncontradaError(
        f"A paragem {nome!r} não existe na linha {self._nome!r}."
      )
    return paragem
  
  # operaçoes 
  def inserir_paragem(self, paragem: Paragem, posicao: int | None = None) -> None:
    # insere uma paragem na linha
    # se a posicao nao for indicada insere no fim
    if self.contem_paragem(paragem.nome):
      raise ParagemDuplicadaError(
        f"A paragem {paragem.nome!r} já existe na linha {self._nome!r}."
      )
      
    if posicao is None:
      self._paragens.inserir_fim(paragem)
    else:
      self._paragens.inserir_posicao(paragem, posicao)
    
    
  def remover_paragem(self, nome: str) -> Paragem:
    paragem = self._localizar(nome)
    if paragem is None:
      raise ParagemNaoEncontradaError(
        f"A paragem {nome!r} não existe na linha {self._nome!r}."
      )
    self._paragens.remover_valor(paragem)
    return paragem
  
  def listar_percurso(self) -> ListaLigada[Paragem]:
    copia: ListaLigada[Paragem] = ListaLigada()
    for paragem in self._paragens:
      copia.inserir_fim(paragem)
    return copia
  
 # grafo não dirigido representativo da linha
  def construir_grafo(self) -> Grafo:
    grafo = Grafo(dirigido=False)
    anterior: Paragem | None = None
    for paragem in self._paragens:
      grafo.adicionar_no(paragem.nome)
      if anterior is not None:
        grafo.adicionar_aresta(anterior.nome, paragem.nome)
      anterior = paragem
    return grafo
  
  def _localizar(self, nome: str) -> Paragem | None:
    for paragem in self._paragens:
      if paragem.nome == nome:
        return paragem
    return None

  def __repr__(self) -> str:
    nomes = " -> ".join(p.nome for p in self._paragens)
    return f"Linha({self._nome!r}, [{nomes}])"