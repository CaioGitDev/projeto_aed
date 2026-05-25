"""
Testes unitários da classeFila
Para executar estes testes, utilizar o comando: pytest testes/test_fila.py -v
"""
 
import pytest
 
from src.estruturas.fila import Fila, FilaVaziaError
 
 
 # Teste para inicialização da fila
class TestConstrucao:
  def test_fila_recem_criada_esta_vazia(self):
    fila: Fila[int] = Fila()
    assert fila.esta_vazia()
    assert fila.tamanho == 0
    assert len(fila) == 0

  def test_iteracao_em_fila_vazia_nao_produz_elementos(self):
    fila: Fila[int] = Fila()
    assert list(fila) == []
    
    
# Testes FIFO
class TestFIFO:
  def test_primeiro_a_entrar_primeiro_a_sair(self):
    fila: Fila[str] = Fila()
    fila.enfileirar("passageiro1")
    fila.enfileirar("passageiro2")
    fila.enfileirar("passageiro3")
    assert fila.desenfileirar() == "passageiro1"
    assert fila.desenfileirar() == "passageiro2"
    assert fila.desenfileirar() == "passageiro3"
    assert fila.esta_vazia()
    
  def test_tamanho_atualiza_corretamente(self):
    fila: Fila[int] = Fila()
    assert fila.tamanho == 0
    fila.enfileirar(1)
    assert fila.tamanho == 1
    fila.enfileirar(2)
    assert fila.tamanho == 2
    fila.desenfileirar()
    assert fila.tamanho == 1
    
  def test_alternancia_entrar_sair(self):
    # validar os ponteiros de frente e tras em cenários alternados
    fila: Fila[int] = Fila()
    fila.enfileirar(1)
    fila.enfileirar(2)
    assert fila.desenfileirar() == 1
    fila.enfileirar(3)
    assert fila.desenfileirar() == 2
    assert fila.desenfileirar() == 3
    assert fila.esta_vazia()
    
# teste consulta frente
class TestFrente:
  def test_frente_nao_remove(self):
    fila: Fila[str] = Fila()
    fila.enfileirar("primeiro")
    fila.enfileirar("segundo")
    assert fila.frente() == "primeiro"
    assert fila.tamanho == 2
    assert fila.desenfileirar() == "primeiro"
    assert fila.frente() == "segundo"
    assert fila.tamanho == 1
    
  def test_frente_em_fila_vazia_lanca_erro(self):
    fila: Fila[int] = Fila()
    with pytest.raises(FilaVaziaError):
      fila.frente()
      
# Testes casos limite
class TestCasosLimite:
  def test_ciclo_vazio_um_vazio(self):
    fila: Fila[int] = Fila()
    fila.enfileirar(1)
    assert fila.desenfileirar() == 1
    assert fila.esta_vazia()
    fila.enfileirar(2)
    assert fila.frente() == 2
    assert fila.tamanho == 1
    
    
# teste caso real mais proximo possivel do exercico proposto
class TestCasoReal:
  def test_fila_de_passageiros_numa_paragem(self):
    fila: Fila[str] = Fila()
    fila.enfileirar("passageiro1")
    fila.enfileirar("passageiro2")
    fila.enfileirar("passageiro3")
    assert fila.tamanho == 3
    
    # consultar quem esta em espera 
    assert list(fila.listar()) == ["passageiro1", "passageiro2", "passageiro3"]
    
    # primeiro a embarcar
    embarcado = fila.desenfileirar()
    assert embarcado == "passageiro1"
    
    # chega mais um passageiro
    fila.enfileirar("passageiro4")
    
    # proximo a embarcar deve ser passageiro2
    assert fila.desenfileirar() == "passageiro2"
    
    # em espera
    assert list(fila.listar()) == ["passageiro3", "passageiro4"]
    assert fila.tamanho == 2