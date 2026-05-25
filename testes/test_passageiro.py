"""
Testes unitários da entidade Passageiro.

Execução:
    pytest testes/test_passageiro.py -v
"""

import dataclasses

import pytest

from src.dominio.passageiro import Passageiro
from src.estruturas.fila import Fila
from src.estruturas.lista_ligada import ListaLigada


# ----------------------------------------------------------------------
# Construção
# ----------------------------------------------------------------------


class TestConstrucao:
  def test_cria_passageiro_com_nome(self):
    p = Passageiro("Caio")
    assert p.nome == "Caio"

  def test_str_devolve_o_nome(self):
    p = Passageiro("Caio")
    assert str(p) == "Passageiro(nome='Caio')"


# ----------------------------------------------------------------------
# Imutabilidade
# ----------------------------------------------------------------------


class TestImutabilidade:
  def test_nao_permite_alterar_nome(self):
    p = Passageiro("Caio")
    with pytest.raises(dataclasses.FrozenInstanceError):
      p.nome = "Sofia" 


# ----------------------------------------------------------------------
# Igualdade e hash
# ----------------------------------------------------------------------


class TestIgualdade:
  def test_passageiros_com_mesmo_nome_sao_iguais(self):
    assert Passageiro("Sofia") == Passageiro("Sofia")

  def test_passageiros_com_nomes_diferentes_sao_distintos(self):
    assert Passageiro("Caio") != Passageiro("Sofia")

  def test_hash_consistente_com_igualdade(self):
    # Objetos iguais têm de ter o mesmo hash.
    assert hash(Passageiro("Caio")) == hash(Passageiro("Caio"))

  def test_utilizavel_em_set(self):
    conjunto = {Passageiro("Caio"), Passageiro("Caio"), Passageiro("Sofia")}
    # "Caio" duplicado deve retornar num único elemento.
    assert len(conjunto) == 2


# ----------------------------------------------------------------------
# Validação
# ----------------------------------------------------------------------


class TestValidacao:
  def test_nome_vazio_lanca_erro(self):
    with pytest.raises(ValueError):
      Passageiro("")

  def test_nome_so_com_espacos_lanca_erro(self):
    with pytest.raises(ValueError):
      Passageiro("   ")


# ----------------------------------------------------------------------
# Integração com estruturas de dados
# ----------------------------------------------------------------------


class TestIntegracaoEstruturas:
  def test_passageiro_numa_fila(self):
    fila: Fila[Passageiro] = Fila()
    fila.enfileirar(Passageiro("Caio"))
    fila.enfileirar(Passageiro("Nadine"))
    assert fila.desenfileirar() == Passageiro("Caio")
    assert fila.frente() == Passageiro("Nadine")

  def test_remover_passageiro_por_igualdade_de_nome(self):
    # A remoção por valor deve funcionar fornecendo um passageiro
    # equivalente (mesmo nome), graças à igualdade por nome.
    lista: ListaLigada[Passageiro] = ListaLigada()
    lista.inserir_fim(Passageiro("Caio"))
    lista.inserir_fim(Passageiro("Nadine"))
    lista.remover_valor(Passageiro("Caio"))
    assert list(lista) == [Passageiro("Nadine")]

  def test_contains_por_nome(self):
    lista: ListaLigada[Passageiro] = ListaLigada()
    lista.inserir_fim(Passageiro("Caio"))
    assert Passageiro("Caio") in lista
    assert Passageiro("Sofia") not in lista