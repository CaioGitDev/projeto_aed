# pytest testes/test_simulador.py -v

import pytest

from src.dominio.autocarro import Autocarro
from src.dominio.linha import Linha
from src.dominio.paragem import Paragem
from src.dominio.passageiro import Passageiro
from src.simulacao.simulador import (
  EventoSimulacao,
  FimDaLinhaError,
  LinhaVaziaError,
  Simulador,
  TipoEvento,
)

def _linha_basica():
  """Cria uma linha com 3 paragens: A, B, C."""
  linha = Linha("L1")
  for nome in ["A", "B", "C"]:
    linha.inserir_paragem(Paragem(nome))
  return linha


def _tipos(eventos):
  """Extrai a sequência de tipos de uma ListaLigada de eventos."""
  return [e.tipo for e in eventos]

class TestConstrucao:
  def test_estado_inicial(self):
    sim = Simulador(_linha_basica(), Autocarro(capacidade=5))
    assert sim.autocarro.posicao_atual is None
    assert not sim.terminou()

  def test_simulador_em_linha_vazia_nao_falha_a_construir(self):
    sim = Simulador(Linha("L1"), Autocarro(capacidade=5))
    assert sim.terminou() 


class TestAvancarUmaParagem:
  def test_primeiro_avanco_posiciona_no_topo(self):
    linha = _linha_basica()
    autocarro = Autocarro(capacidade=5)
    sim = Simulador(linha, autocarro)

    eventos = sim.avancar_uma_paragem()

    assert autocarro.posicao_atual.nome == "A"
    # Primeira chegada: como o autocarro estava vazio, nada a
    # desembarcar; como não havia ninguém em A, nada a embarcar.
    assert _tipos(eventos) == [
      TipoEvento.CHEGADA,
      TipoEvento.NAO_HA_QUEM_DESEMBARCAR,
      TipoEvento.NAO_HA_QUEM_EMBARCAR,
    ]

  def test_embarque_quando_ha_fila(self):
    linha = _linha_basica()
    linha.obter_paragem("A").adicionar_passageiro(Passageiro("Caio"))
    sim = Simulador(linha, Autocarro(capacidade=5))

    eventos = sim.avancar_uma_paragem()

    # A Caio deve ter embarcado.
    eventos_lista = list(eventos)
    assert eventos_lista[-1].tipo == TipoEvento.EMBARQUE
    assert eventos_lista[-1].passageiro == "Caio"
    assert sim.autocarro.lotacao() == 1

  def test_desembarque_em_paragem_seguinte(self):
    linha = _linha_basica()
    linha.obter_paragem("A").adicionar_passageiro(Passageiro("Caio"))
    sim = Simulador(linha, Autocarro(capacidade=5))

    # Avança até A: Caio embarca.
    sim.avancar_uma_paragem()
    # Avança até B: Caio deve desembarcar (o primeiro a entrar, sai).
    eventos = sim.avancar_uma_paragem()

    eventos_lista = list(eventos)
    desembarques = [e for e in eventos_lista if e.tipo == TipoEvento.DESEMBARQUE]
    assert len(desembarques) == 1
    assert desembarques[0].passageiro == "Caio"
    assert sim.autocarro.lotacao() == 0

  def test_autocarro_cheio_nao_embarca(self):
    linha = _linha_basica()
    # Em A há um passageiro à espera, mas o autocarro só leva 1 e
    # já tem alguém a bordo (que não foi desembarcado).
    linha.obter_paragem("A").adicionar_passageiro(Passageiro("Caio"))
    # Vamos forçar o autocarro a chegar a A já cheio:
    autocarro = Autocarro(capacidade=1)
    autocarro.embarcar(Passageiro("PreEmbarcado"))
    sim = Simulador(linha, autocarro)

    # Avança a A com desembarque DESLIGADO: o passageiro pré-embarcado
    # permanece, o autocarro continua cheio.
    eventos = sim.avancar_uma_paragem(desembarcar_um=False)
    # O último evento deve ser AUTOCARRO_CHEIO.
    eventos_lista = list(eventos)
    assert eventos_lista[-1].tipo == TipoEvento.AUTOCARRO_CHEIO
    # A Caio deve continuar em espera (não embarcou).
    assert linha.obter_paragem("A").numero_em_espera() == 1

  def test_desligar_desembarque(self):
    linha = _linha_basica()
    linha.obter_paragem("A").adicionar_passageiro(Passageiro("Caio"))
    sim = Simulador(linha, Autocarro(capacidade=5))
    sim.avancar_uma_paragem() 
    eventos = sim.avancar_uma_paragem(desembarcar_um=False)
    assert TipoEvento.DESEMBARQUE not in _tipos(eventos)
    assert sim.autocarro.lotacao() == 1

  def test_desligar_embarque(self):
    linha = _linha_basica()
    linha.obter_paragem("A").adicionar_passageiro(Passageiro("Caio"))
    sim = Simulador(linha, Autocarro(capacidade=5))
    eventos = sim.avancar_uma_paragem(embarcar_um=False)
    assert TipoEvento.EMBARQUE not in _tipos(eventos)
    assert linha.obter_paragem("A").numero_em_espera() == 1

  def test_terminado_apos_ultima_paragem(self):
    sim = Simulador(_linha_basica(), Autocarro(capacidade=5))
    sim.avancar_uma_paragem()
    sim.avancar_uma_paragem()
    sim.avancar_uma_paragem()
    assert sim.terminou()
    with pytest.raises(FimDaLinhaError):
      sim.avancar_uma_paragem()

class TestErros:
  def test_simular_em_linha_vazia_lanca_erro(self):
    sim = Simulador(Linha("L1"), Autocarro(capacidade=5))
    with pytest.raises(LinhaVaziaError):
      sim.avancar_uma_paragem()



class TestPercursoCompleto:
  def test_termina_no_fim_da_linha(self):
    sim = Simulador(_linha_basica(), Autocarro(capacidade=5))
    _ = sim.simular_percurso_completo()
    assert sim.terminou()
    assert sim.autocarro.posicao_atual.nome == "C"

  def test_eventos_incluem_chegada_a_cada_paragem(self):
    sim = Simulador(_linha_basica(), Autocarro(capacidade=5))
    eventos = list(sim.simular_percurso_completo())
    chegadas = [e for e in eventos if e.tipo == TipoEvento.CHEGADA]
    assert [e.paragem for e in chegadas] == ["A", "B", "C"]


class TestCenarioIntegrado:
  def test_passageiros_em_varias_paragens(self):
    linha = Linha("L1")
    for nome in ["A", "B", "C", "D"]:
        linha.inserir_paragem(Paragem(nome))
    linha.obter_paragem("A").adicionar_passageiro(Passageiro("Caio"))
    linha.obter_paragem("C").adicionar_passageiro(Passageiro("Sofia"))
    autocarro = Autocarro(capacidade=2)
    sim = Simulador(linha, autocarro)

    eventos = list(sim.simular_percurso_completo())

    embarques = [e for e in eventos if e.tipo == TipoEvento.EMBARQUE]
    desembarques = [e for e in eventos if e.tipo == TipoEvento.DESEMBARQUE]

    assert {e.passageiro for e in embarques} == {"Caio", "Sofia"}
    nomes_desembarcados = {e.passageiro for e in desembarques}
    assert nomes_desembarcados == {"Caio", "Sofia"}
    assert autocarro.esta_vazio()

  def test_evento_chegada_inclui_estatisticas(self):
      linha = _linha_basica()
      for nome in ["Caio", "Sofia"]:
        linha.obter_paragem("A").adicionar_passageiro(Passageiro(nome))
      sim = Simulador(linha, Autocarro(capacidade=5))
      eventos = list(sim.avancar_uma_paragem())
      chegada = eventos[0]
      assert "0/5" in chegada.detalhe  
      assert "2" in chegada.detalhe    