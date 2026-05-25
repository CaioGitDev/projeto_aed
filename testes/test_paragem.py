# Testes unitarios para a classe Paragem
# executar pytest testes/test_paragem.py -v

import pytest
 
from src.dominio.paragem import Paragem, ParagemVaziaError
from src.dominio.passageiro import Passageiro

# Testes para a criação da paragem
class TestInicializacao:
  def test_cria_paragem_com_nome(self):
    paragem = Paragem("Salvaterra de magos")
    assert paragem.nome == "Salvaterra de magos"
    assert paragem.numero_em_espera() == 0
    assert not paragem.tem_passageiros()

  def test_nome_limpo_sem_espacos(self):
    paragem = Paragem("  Salvaterra de magos  ")
    assert paragem.nome == "Salvaterra de magos"
    
  def test_nome_vazio_levanta_erro(self):
    with pytest.raises(ValueError):
      Paragem("")
  
  def test_nome_espacos_levanta_erro(self):
    with pytest.raises(ValueError):
      Paragem("   ")
      
# Testes para a gestão de passageiros
class TestGestaoPassageiros:
  def test_adicionar_passageiro_incrementa_espera(self):
    paragem = Paragem("Salvaterra de magos")
    paragem.adicionar_passageiro(Passageiro("Catarina"))
    assert paragem.numero_em_espera() == 1
    assert paragem.tem_passageiros()
    
  def test_embarcar_respeita_fifo(self):
    paragem = Paragem("Foros de salvaterra")
    paragem.adicionar_passageiro(Passageiro("Catarina"))
    paragem.adicionar_passageiro(Passageiro("Sofia"))
    assert paragem.embarcar_passageiro() ==Passageiro("Catarina")
    assert paragem.embarcar_passageiro() == Passageiro("Sofia")
    
  def test_embarque_decrementa_espera(self):
    p = Paragem("Marinhais")
    p.adicionar_passageiro(Passageiro("nadine"))
    p.adicionar_passageiro(Passageiro("caio"))
    p.embarcar_passageiro()
    assert p.numero_em_espera() == 1

  def test_embarcar_de_paragem_vazia_lanca_erro(self):
    p = Paragem("Marinhais")
    with pytest.raises(ParagemVaziaError):
      p.embarcar_passageiro()
      
# Consultas
class TestConsulta:
  def test_passageiros_em_espera_pela_ordem_da_fila(self):
    p = Paragem("Benavente")
    for nome in ["Caio", "Sofia", "Nadine"]:
      p.adicionar_passageiro(Passageiro(nome))
    em_espera = list(p.passageiros_em_espera())
    assert em_espera == [
      Passageiro("Caio"),
      Passageiro("Sofia"),
      Passageiro("Nadine"),
    ]

  def test_consulta_nao_remove(self):
    p = Paragem("Benavente")
    p.adicionar_passageiro(Passageiro("Caio"))
    _ = p.passageiros_em_espera()
    assert p.numero_em_espera() == 1
    

# teste integrado
class TestCenarioIntegrado:
  def test_chegadas_e_embarques_intercalados(self):
    paragem = Paragem("Salvaterra de magos")
    
    # Chegada de passageiros
    paragem.adicionar_passageiro(Passageiro("Catarina"))
    paragem.adicionar_passageiro(Passageiro("Sofia"))
    paragem.adicionar_passageiro(Passageiro("Nadine"))
    assert paragem.numero_em_espera() == 3
    
    # o autocarro chega e embarca um passageiro
    embarcado = paragem.embarcar_passageiro()
    assert embarcado == Passageiro("Catarina")
    
    # chegou outro passageiro enquanto o autocarro estava parado
    paragem.adicionar_passageiro(Passageiro("Caio"))
    
    # em espera estão os 3 restantes, na ordem correta
    assert list(paragem.passageiros_em_espera()) == [
      Passageiro("Sofia"),
      Passageiro("Nadine"),
      Passageiro("Caio"),
    ]
    assert paragem.numero_em_espera() == 3