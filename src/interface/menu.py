from __future__ import annotations
 
from dataclasses import dataclass, field
from typing import Callable, Optional
 
from src.algoritmos.ordenacao import (
  bubble_sort,
  insertion_sort,
  selection_sort,
)
from src.algoritmos.pesquisa import bfs_caminho
from src.dominio.autocarro import Autocarro
from src.dominio.linha import Linha, ParagemDuplicadaError, ParagemNaoEncontradaError
from src.dominio.paragem import Paragem
from src.dominio.passageiro import Passageiro
from src.estruturas.grafo import NoInexistenteError
from src.simulacao.simulador import (
  EventoSimulacao,
  FimDaLinhaError,
  LinhaVaziaError,
  Simulador,
  TipoEvento,
)

# LEITURA E escrita do sistema
class IO:
  def __init__(
    self,
    leitor: Callable[[str], str] = input,
    escritor: Callable[[str], None] = print,
  ) -> None:
    self._leitor = leitor
    self._escritor = escritor

  def ler(self, prompt: str = "") -> str:
    return self._leitor(prompt)

  def escrever(self, texto: str = "") -> None:
    self._escritor(texto)
    
def _ler_texto(io: IO, prompt: str, *, permitir_vazio: bool = False) -> str | None:
  """
  Lê texto do utilizador, removendo espaços nas extremidades. Devolve
  `None` se `permitir_vazio=False` e o utilizador entregar uma string
  vazia; nesse caso, imprime mensagem de erro.
  """
  valor = io.ler(prompt).strip()
  if not valor and not permitir_vazio:
    io.escrever("  Entrada inválida: o valor não pode ser vazio.")
    return None
  return valor
 
def _ler_inteiro(io: IO, prompt: str, *, minimo: int | None = None) -> int | None:
  """
  Lê um inteiro do utilizador. Devolve `None` em caso de entrada
  inválida (não numérica ou abaixo do mínimo), imprimindo mensagem.
  """
  bruto = io.ler(prompt).strip()
  try:
    valor = int(bruto)
  except ValueError:
    io.escrever("  Entrada inválida: indique um número inteiro.")
    return None
  if minimo is not None and valor < minimo:
    io.escrever(f"  Entrada inválida: o valor deve ser >= {minimo}.")
    return None
  return valor


# estado da aplicação
@dataclass
class EstadoAplicacao:
  """Estado global da sessão de utilização."""
  linha: Optional[Linha] = None
  autocarro: Optional[Autocarro] = None
 
 
def _exige_linha(estado: EstadoAplicacao, io: IO) -> bool:
  """Verifica que existe uma linha; caso contrário, avisa e devolve False."""
  if estado.linha is None:
    io.escrever("  Ainda não foi criada nenhuma linha. Use a opção 1.")
    return False
  return True

 
def _exige_autocarro(estado: EstadoAplicacao, io: IO) -> bool:
  """Verifica que existe um autocarro; caso contrário, avisa."""
  if estado.autocarro is None:
    io.escrever(
      "  Ainda não foi configurado autocarro. Use a opção 1 para criar a linha."
    )
    return False
  return True

 # formatavao  de eventos
 
_ICONES_EVENTO = {
  TipoEvento.CHEGADA: "[CHEGADA]",
  TipoEvento.DESEMBARQUE: "[DESCE  ]",
  TipoEvento.EMBARQUE: "[SOBE   ]",
  TipoEvento.NAO_HA_QUEM_DESEMBARCAR: "[       ]",
  TipoEvento.NAO_HA_QUEM_EMBARCAR: "[       ]",
  TipoEvento.AUTOCARRO_CHEIO: "[CHEIO  ]",
}
 
 
def _formatar_evento(e: EventoSimulacao) -> str:
  icone = _ICONES_EVENTO.get(e.tipo, "[       ]")
  if e.tipo == TipoEvento.CHEGADA:
    texto = f"Chegada a {e.paragem} ({e.detalhe})"
  elif e.tipo == TipoEvento.DESEMBARQUE:
    texto = f"{e.passageiro} desceu em {e.paragem}"
  elif e.tipo == TipoEvento.EMBARQUE:
    texto = f"{e.passageiro} embarcou em {e.paragem}"
  elif e.tipo == TipoEvento.NAO_HA_QUEM_DESEMBARCAR:
    texto = f"Ninguém para desembarcar em {e.paragem}"
  elif e.tipo == TipoEvento.NAO_HA_QUEM_EMBARCAR:
    texto = f"Ninguém em espera em {e.paragem}"
  elif e.tipo == TipoEvento.AUTOCARRO_CHEIO:
    texto = f"Autocarro cheio em {e.paragem} ({e.detalhe})"
  else:
    texto = str(e)
  return f"  {icone} {texto}"


def _opcao_criar_linha(estado: EstadoAplicacao, io: IO) -> None:
  nome = _ler_texto(io, "Nome da linha: ")
  if nome is None:
    return
  capacidade = _ler_inteiro(io, "Capacidade do autocarro: ", minimo=1)
  if capacidade is None:
    return
  try:
    estado.linha = Linha(nome)
    estado.autocarro = Autocarro(capacidade=capacidade)
  except ValueError as exc:
    io.escrever(f"  Erro: {exc}")
    return
  io.escrever(f"  Linha '{estado.linha.nome}' criada com autocarro de capacidade {capacidade}.")

def _opcao_adicionar_paragem(estado: EstadoAplicacao, io: IO) -> None:
  if not _exige_linha(estado, io):
    return
  nome = _ler_texto(io, "Nome da nova paragem: ")
  if nome is None:
    return
  try:
    estado.linha.inserir_paragem(Paragem(nome))
  except ParagemDuplicadaError as exc:
    io.escrever(f"  Erro: {exc}")
    return
  io.escrever(f"  Paragem '{nome}' adicionada ao fim da linha.")

def _opcao_remover_paragem(estado: EstadoAplicacao, io: IO) -> None:
  if not _exige_linha(estado, io):
    return
  nome = _ler_texto(io, "Nome da paragem a remover: ")
  if nome is None:
    return
  try:
    estado.linha.remover_paragem(nome)
  except ParagemNaoEncontradaError as exc:
    io.escrever(f"  Erro: {exc}")
    return
  io.escrever(f"  Paragem '{nome}' removida.")

def _opcao_adicionar_passageiro(estado: EstadoAplicacao, io: IO) -> None:
  if not _exige_linha(estado, io):
    return
  nome_paragem = _ler_texto(io, "Nome da paragem: ")
  if nome_paragem is None:
    return
  nome_passageiro = _ler_texto(io, "Nome do passageiro: ")
  if nome_passageiro is None:
    return
  try:
      paragem = estado.linha.obter_paragem(nome_paragem)
  except ParagemNaoEncontradaError as exc:
    io.escrever(f"  Erro: {exc}")
    return
  try:
    paragem.adicionar_passageiro(Passageiro(nome_passageiro))
  except ValueError as exc:
    io.escrever(f"  Erro: {exc}")
    return
  io.escrever(
    f"  Passageiro '{nome_passageiro}' adicionado à fila de '{nome_paragem}' "
    f"(agora {paragem.numero_em_espera()} em espera)."
  )

def _opcao_simular_chegada(estado: EstadoAplicacao, io: IO) -> None:
  if not _exige_linha(estado, io) or not _exige_autocarro(estado, io):
    return
  # Cria-se ou reutiliza-se um simulador associado ao estado.
  # Para simplificar, criamos um simulador novo a cada vez, mas
  # baseado no índice atual do autocarro (calculado pela posição).
  simulador = _obter_ou_criar_simulador(estado)
  try:
    eventos = simulador.avancar_uma_paragem()
  except (LinhaVaziaError, FimDaLinhaError) as exc:
    io.escrever(f"  Erro: {exc}")
    return
  for e in eventos:
    io.escrever(_formatar_evento(e))
 
def _obter_ou_criar_simulador(estado: EstadoAplicacao) -> Simulador:
  sim = getattr(estado, "_simulador", None)
  if sim is None or sim.linha is not estado.linha or sim.autocarro is not estado.autocarro:
    sim = Simulador(estado.linha, estado.autocarro)
    estado._simulador = sim  # type: ignore[attr-defined]
  return sim
 
def _opcao_ordenar_paragens(estado: EstadoAplicacao, io: IO) -> None:
  if not _exige_linha(estado, io):
    return
  io.escrever("  Critério:")
  io.escrever("    1) por nome")
  io.escrever("    2) por número de passageiros (decrescente)")
  criterio = _ler_inteiro(io, "  Escolha: ")
  if criterio not in (1, 2):
    if criterio is not None:
      io.escrever("  Critério inválido.")
    return

  io.escrever("  Algoritmo:")
  io.escrever("    1) Bubble Sort")
  io.escrever("    2) Insertion Sort")
  io.escrever("    3) Selection Sort")
  alg_escolha = _ler_inteiro(io, "  Escolha: ")
  algoritmos = {1: bubble_sort, 2: insertion_sort, 3: selection_sort}
  if alg_escolha not in algoritmos:
    if alg_escolha is not None:
      io.escrever("  Algoritmo inválido.")
    return
  algoritmo = algoritmos[alg_escolha]

  if criterio == 1:
    ordenadas = algoritmo(estado.linha.listar_percurso(), chave=lambda p: p.nome)
  else:
    ordenadas = algoritmo(
      estado.linha.listar_percurso(),
      chave=lambda p: p.numero_em_espera(),
      reverso=True,
    )

  io.escrever("  Resultado:")
  for p in ordenadas:
    io.escrever(f"    {p.nome:<25} ({p.numero_em_espera()} em espera)")
 
def _opcao_mostrar_estado(estado: EstadoAplicacao, io: IO) -> None:
  if not _exige_linha(estado, io):
    return
  linha = estado.linha
  io.escrever(f"  Linha: {linha.nome}")
  io.escrever(f"  Número de paragens: {linha.numero_paragens}")
  if estado.autocarro is not None:
    pos = (
      estado.autocarro.posicao_atual.nome
      if estado.autocarro.posicao_atual is not None
      else "-"
    )
    io.escrever(
      f"  Autocarro: lotação {estado.autocarro.lotacao()}/"
      f"{estado.autocarro.capacidade}, posição: {pos}"
    )
  if linha.esta_vazia():
    io.escrever("  (Linha sem paragens)")
    return
  io.escrever("  Percurso:")
  for p in linha.listar_percurso():
    io.escrever(f"    - {p.nome:<25} ({p.numero_em_espera()} em espera)")

def _opcao_calcular_percurso(estado: EstadoAplicacao, io: IO) -> None:
  if not _exige_linha(estado, io):
    return
  origem = _ler_texto(io, "Paragem de origem: ")
  if origem is None:
    return
  destino = _ler_texto(io, "Paragem de destino: ")
  if destino is None:
    return
  grafo = estado.linha.construir_grafo()
  try:
    caminho = bfs_caminho(grafo, origem, destino)
  except NoInexistenteError as exc:
    io.escrever(f"  Erro: {exc}")
    return
  if caminho is None:
    io.escrever(f"  Não existe caminho entre '{origem}' e '{destino}'.")
    return
  nomes = list(caminho)
  arestas = len(nomes) - 1
  io.escrever(f"  Caminho ({arestas} {'aresta' if arestas == 1 else 'arestas'}):")
  io.escrever("    " + " -> ".join(nomes))
 
def _opcao_comparar_algoritmos(estado: EstadoAplicacao, io: IO) -> None:
  io.escrever("  A executar comparação (pode demorar alguns segundos)...")
  from src.algoritmos.benchmark import (
    TAMANHOS_DEFAULT,
    executar_benchmark,
    gerar_grafico,
    imprimir_tabela,
  )
  import os
  resultados = executar_benchmark()
  import io as iolib
  import contextlib
  buffer = iolib.StringIO()
  with contextlib.redirect_stdout(buffer):
    imprimir_tabela(resultados, TAMANHOS_DEFAULT)
  for linha_texto in buffer.getvalue().splitlines():
    io.escrever(linha_texto)
  caminho = os.path.join("relatorio", "imagens", "benchmark_ordenacao.png")
  os.makedirs(os.path.dirname(caminho), exist_ok=True)
  gerar_grafico(resultados, TAMANHOS_DEFAULT, caminho)
  io.escrever(f"  Gráfico guardado em: {caminho}")
 
def _opcao_visualizar_topologia(estado: EstadoAplicacao, io: IO) -> None:
  if not _exige_linha(estado, io):
    return
  if estado.linha.esta_vazia():
    io.escrever("  Linha vazia: nada a visualizar.")
    return
  try:
    import os
    from src.interface.visualizacao import desenhar_linha
  except ImportError as exc:
    io.escrever(f"  Erro: módulo de visualização indisponível ({exc}).")
    return
  caminho = os.path.join("relatorio", "imagens", "topologia.png")
  os.makedirs(os.path.dirname(caminho), exist_ok=True)
  desenhar_linha(estado.linha, caminho)
  io.escrever(f"  Imagem guardada em: {caminho}")
 
 

_MENU = """
========================================================
   Sistema de Gestão de Linha de Autocarros
========================================================
  1.  Criar linha de autocarro
  2.  Adicionar paragem
  3.  Remover paragem
  4.  Adicionar passageiro a uma paragem
  5.  Simular chegada do autocarro à próxima paragem
  6.  Ordenar paragens (por nome ou nº de passageiros)
  7.  Mostrar estado atual da linha
  8.  Calcular percurso entre duas paragens (BFS)
  9.  Comparar algoritmos de ordenação (benchmark)
 10.  Visualizar topologia da linha (imagem)
  0.  Sair
"""
 
 
def executar(io: IO | None = None) -> None:
  """
  Ciclo principal da aplicação. Continua até o utilizador escolher
  a opção 0.
  """
  if io is None:
    io = IO()
  estado = EstadoAplicacao()

  while True:
    io.escrever(_MENU)
    escolha = _ler_inteiro(io, "  Escolha uma opção: ")
    if escolha is None:
      continue
    match escolha:
      case 0:
        io.escrever("  Até à próxima.")
        return
      case 1:
        _opcao_criar_linha(estado, io)
      case 2:
        _opcao_adicionar_paragem(estado, io)
      case 3:
        _opcao_remover_paragem(estado, io)
      case 4:
        _opcao_adicionar_passageiro(estado, io)
      case 5:
        _opcao_simular_chegada(estado, io)
      case 6:
        _opcao_ordenar_paragens(estado, io)
      case 7:
        _opcao_mostrar_estado(estado, io)
      case 8:
        _opcao_calcular_percurso(estado, io)
      case 9:
        _opcao_comparar_algoritmos(estado, io)
      case 10:
        _opcao_visualizar_topologia(estado, io)
      case _:
        io.escrever("  Opção inválida.")
 
 
if __name__ == "__main__":
  executar()











