# pytest testes/test_menu.py -v
from collections import deque
 
import pytest
 
from src.dominio.passageiro import Passageiro
from src.interface.menu import (
  EstadoAplicacao,
  IO,
  _opcao_adicionar_paragem,
  _opcao_adicionar_passageiro,
  _opcao_calcular_percurso,
  _opcao_criar_linha,
  _opcao_mostrar_estado,
  _opcao_ordenar_paragens,
  _opcao_remover_paragem,
  _opcao_simular_chegada,
  executar,
)

class IOFake(IO):
  def __init__(self, respostas: list[str]) -> None:
    self._respostas = deque(respostas)
    self.saida: list[str] = []

    def _ler(prompt: str) -> str:
      self.saida.append(f"PROMPT: {prompt}")
      if not self._respostas:
        raise AssertionError("IOFake ficou sem respostas.")
      return self._respostas.popleft()

    def _escrever(texto: str = "") -> None:
      self.saida.append(texto)

    super().__init__(leitor=_ler, escritor=_escrever)

  @property
  def texto_completo(self) -> str:
    return "\n".join(self.saida)
  

class TestCriarLinha:
  def test_cria_linha_e_autocarro(self):
    io = IOFake(["Linha 728", "10"])
    estado = EstadoAplicacao()
    _opcao_criar_linha(estado, io)
    assert estado.linha is not None
    assert estado.linha.nome == "Linha 728"
    assert estado.autocarro is not None
    assert estado.autocarro.capacidade == 10

  def test_capacidade_invalida(self):
    io = IOFake(["L1", "0"])
    estado = EstadoAplicacao()
    _opcao_criar_linha(estado, io)
    # Não deve criar nada.
    assert estado.linha is None
    assert estado.autocarro is None

  def test_nome_vazio(self):
    io = IOFake([""])
    estado = EstadoAplicacao()
    _opcao_criar_linha(estado, io)
    assert estado.linha is None
    
class TestAdicionarParagem:
  def test_adiciona_a_linha_existente(self):
    io = IOFake(["Linha 728", "10"])
    estado = EstadoAplicacao()
    _opcao_criar_linha(estado, io)
    io = IOFake(["Rossio"])
    _opcao_adicionar_paragem(estado, io)
    assert estado.linha.contem_paragem("Rossio")

  def test_sem_linha_avisa_utilizador(self):
    io = IOFake([])  # Nem chega a pedir input.
    estado = EstadoAplicacao()
    _opcao_adicionar_paragem(estado, io)
    assert any("Ainda não foi criada" in linha for linha in io.saida)

  def test_paragem_duplicada(self):
    io = IOFake(["L1", "5"])
    estado = EstadoAplicacao()
    _opcao_criar_linha(estado, io)
    io = IOFake(["Rossio"])
    _opcao_adicionar_paragem(estado, io)
    io = IOFake(["Rossio"])
    _opcao_adicionar_paragem(estado, io)
    assert any("Erro" in linha for linha in io.saida)
    

class TestRemoverParagem:
  def test_remove_paragem_existente(self):
    estado = EstadoAplicacao()
    _opcao_criar_linha(estado, IOFake(["L1", "5"]))
    _opcao_adicionar_paragem(estado, IOFake(["Rossio"]))
    _opcao_adicionar_paragem(estado, IOFake(["Marquês"]))
    _opcao_remover_paragem(estado, IOFake(["Rossio"]))
    assert not estado.linha.contem_paragem("Rossio")
    assert estado.linha.contem_paragem("Marquês")

  def test_remover_inexistente(self):
    estado = EstadoAplicacao()
    _opcao_criar_linha(estado, IOFake(["L1", "5"]))
    io = IOFake(["FANTASMA"])
    _opcao_remover_paragem(estado, io)
    assert any("Erro" in linha for linha in io.saida)

class TestAdicionarPassageiro:
  def test_adiciona_a_paragem_existente(self):
    estado = EstadoAplicacao()
    _opcao_criar_linha(estado, IOFake(["L1", "5"]))
    _opcao_adicionar_paragem(estado, IOFake(["Rossio"]))
    _opcao_adicionar_passageiro(estado, IOFake(["Rossio", "Ana"]))
    assert estado.linha.obter_paragem("Rossio").numero_em_espera() == 1

  def test_paragem_inexistente(self):
    estado = EstadoAplicacao()
    _opcao_criar_linha(estado, IOFake(["L1", "5"]))
    io = IOFake(["FANTASMA", "Ana"])
    _opcao_adicionar_passageiro(estado, io)
    assert any("Erro" in linha for linha in io.saida)


class TestSimularChegada:
  def test_avanca_para_primeira_paragem(self):
    estado = EstadoAplicacao()
    _opcao_criar_linha(estado, IOFake(["L1", "5"]))
    _opcao_adicionar_paragem(estado, IOFake(["Rossio"]))
    _opcao_adicionar_paragem(estado, IOFake(["Marquês"]))
    io = IOFake([])
    _opcao_simular_chegada(estado, io)
    assert estado.autocarro.posicao_atual.nome == "Rossio"

  def test_segundo_avanco_passa_a_seguinte(self):
    estado = EstadoAplicacao()
    _opcao_criar_linha(estado, IOFake(["L1", "5"]))
    _opcao_adicionar_paragem(estado, IOFake(["Rossio"]))
    _opcao_adicionar_paragem(estado, IOFake(["Marquês"]))
    _opcao_simular_chegada(estado, IOFake([]))
    _opcao_simular_chegada(estado, IOFake([]))
    assert estado.autocarro.posicao_atual.nome == "Marquês"

  def test_fim_da_linha_e_reportado(self):
    estado = EstadoAplicacao()
    _opcao_criar_linha(estado, IOFake(["L1", "5"]))
    _opcao_adicionar_paragem(estado, IOFake(["A"]))
    _opcao_simular_chegada(estado, IOFake([]))
    io = IOFake([])
    _opcao_simular_chegada(estado, io)
    assert any("Erro" in linha for linha in io.saida)
    
class TestOrdenarParagens:
  def test_ordena_por_nome_com_bubble(self):
    estado = EstadoAplicacao()
    _opcao_criar_linha(estado, IOFake(["L1", "5"]))
    for nome in ["Rossio", "Avenida", "Marquês"]:
        _opcao_adicionar_paragem(estado, IOFake([nome]))
    # Critério 1 (nome), Algoritmo 1 (Bubble).
    io = IOFake(["1", "1"])
    _opcao_ordenar_paragens(estado, io)
    # Verifica que os nomes aparecem na saída por ordem alfabética.
    texto = io.texto_completo
    pos_avenida = texto.index("Avenida")
    pos_marques = texto.index("Marquês")
    pos_rossio = texto.index("Rossio")
    assert pos_avenida < pos_marques < pos_rossio
    
class TestMostrarEstado:
  def test_mostra_paragens_existentes(self):
    estado = EstadoAplicacao()
    _opcao_criar_linha(estado, IOFake(["L1", "5"]))
    _opcao_adicionar_paragem(estado, IOFake(["Rossio"]))
    io = IOFake([])
    _opcao_mostrar_estado(estado, io)
    texto = io.texto_completo
    assert "L1" in texto
    assert "Rossio" in texto
    
class TestCalcularPercurso:
  def test_caminho_existente(self):
    estado = EstadoAplicacao()
    _opcao_criar_linha(estado, IOFake(["L1", "5"]))
    for nome in ["A", "B", "C"]:
        _opcao_adicionar_paragem(estado, IOFake([nome]))
    io = IOFake(["A", "C"])
    _opcao_calcular_percurso(estado, io)
    texto = io.texto_completo
    assert "A -> B -> C" in texto

  def test_paragem_inexistente(self):
    estado = EstadoAplicacao()
    _opcao_criar_linha(estado, IOFake(["L1", "5"]))
    _opcao_adicionar_paragem(estado, IOFake(["A"]))
    io = IOFake(["FANTASMA", "A"])
    _opcao_calcular_percurso(estado, io)
    assert any("Erro" in linha for linha in io.saida)
    
class TestSaida:
  def test_opcao_zero_termina(self):
    io = IOFake(["0"])
    # Não deve lançar nada nem entrar num ciclo infinito.
    executar(io)
    assert any("Até à próxima" in linha for linha in io.saida)

  def test_opcao_invalida_continua(self):
    # 99 é inválida; depois 0 para sair.
    io = IOFake(["99", "0"])
    executar(io)
    assert any("inválida" in linha.lower() for linha in io.saida)

  def test_entrada_nao_numerica_continua(self):
    io = IOFake(["abc", "0"])
    executar(io)
    # Deve ter avisado sobre a entrada inválida.
    assert any("inválida" in linha.lower() for linha in io.saida)