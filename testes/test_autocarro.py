# TEstes para a classe Autocarro
# pytest testes/test_autocarro.py -v

import pytest
 
from src.dominio.autocarro import (
    Autocarro,
    AutocarroCheioError,
    AutocarroVazioError,
)
from src.dominio.paragem import Paragem
from src.dominio.passageiro import Passageiro


# inicialização

class TestConstrucao:
  def test_estado_inicial(self):
    autocarro = Autocarro(capacidade=10)
    assert autocarro.capacidade == 10
    assert autocarro.lotacao() == 0
    assert autocarro.esta_vazio()
    assert not autocarro.esta_cheio()
    assert autocarro.lugares_livres() == 10
    assert autocarro.posicao_atual is None

  def test_capacidade_zero_lanca_erro(self):
    with pytest.raises(ValueError):
      Autocarro(capacidade=0)

  def test_capacidade_negativa_lanca_erro(self):
    with pytest.raises(ValueError):
      Autocarro(capacidade=-5)
      
class TestEmbarque:
  def test_embarcar_incrementa_lotacao(self):
    autocarro = Autocarro(capacidade=3)
    autocarro.embarcar(Passageiro("Caio"))
    assert autocarro.lotacao() == 1
    assert autocarro.lugares_livres() == 2

  def test_embarcar_ate_encher(self):
    autocarro = Autocarro(capacidade=2)
    autocarro.embarcar(Passageiro("Caio"))
    autocarro.embarcar(Passageiro("Sofia"))
    assert autocarro.esta_cheio()
    assert autocarro.lugares_livres() == 0

  def test_embarcar_com_lotacao_esgotada_lanca_erro(self):
    autocarro = Autocarro(capacidade=1)
    autocarro.embarcar(Passageiro("Caio"))
    with pytest.raises(AutocarroCheioError):
      autocarro.embarcar(Passageiro("Sofia"))
      
class TestDesembarque:
  def test_desembarque_individual_e_fifo(self):
    autocarro = Autocarro(capacidade=5)
    autocarro.embarcar(Passageiro("Nadine"))
    autocarro.embarcar(Passageiro("Sofia"))
    # O primeiro a entrar é o primeiro a sair.
    assert autocarro.desembarcar_passageiro() == Passageiro("Nadine")
    assert autocarro.lotacao() == 1
 
  def test_desembarcar_de_vazio_lanca_erro(self):
    autocarro = Autocarro(capacidade=5)
    with pytest.raises(AutocarroVazioError):
      autocarro.desembarcar_passageiro()

  def test_desembarcar_todos(self):
    autocarro = Autocarro(capacidade=5)
    for nome in ["Nadine", "Sofia", "Caio"]:
      autocarro.embarcar(Passageiro(nome))
    descidos = list(autocarro.desembarcar_todos())
    assert descidos == [
      Passageiro("Nadine"),
      Passageiro("Sofia"),
      Passageiro("Caio"),
    ]
    assert autocarro.esta_vazio()

  def test_desembarcar_todos_de_vazio_devolve_lista_vazia(self):
    autocarro = Autocarro(capacidade=5)
    assert list(autocarro.desembarcar_todos()) == []

  def test_lugares_libertam_apos_desembarque(self):
    autocarro = Autocarro(capacidade=2)
    autocarro.embarcar(Passageiro("Nadine"))
    autocarro.embarcar(Passageiro("Sofia"))
    assert autocarro.esta_cheio()
    autocarro.desembarcar_passageiro()
    # Após descer um, há lugar para novo embarque.
    assert not autocarro.esta_cheio()
    autocarro.embarcar(Passageiro("Caio"))
    assert autocarro.lotacao() == 2
    
    
    
class TestMovimentacao:
  def test_mover_para_atualiza_posicao(self):
    autocarro = Autocarro(capacidade=5)
    salvaterra = Paragem("Salvaterra de magos")
    autocarro.mover_para(salvaterra)
    assert autocarro.posicao_atual is salvaterra
    assert autocarro.posicao_atual.nome == "Salvaterra de magos"

  def test_mover_entre_paragens(self):
    autocarro = Autocarro(capacidade=5)
    autocarro.mover_para(Paragem("Salvaterra de magos"))
    autocarro.mover_para(Paragem("Marinhais"))
    assert autocarro.posicao_atual.nome == "Marinhais"