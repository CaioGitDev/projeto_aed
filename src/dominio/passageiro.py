"""
Entidade Passageiro.
 
Representa um passageiro do sistema de transportes, identificado pelo
seu nome. A entidade é imutável (`frozen=True`): um passageiro não muda
de identidade ao longo da simulação.

"""
 
from __future__ import annotations
 
from dataclasses import dataclass
 
 
@dataclass(frozen=True)
class Passageiro:
  # passageiro é identificado pelo seu nome
  # atributo `nome` nao pode ser vazio ou conter apenas espaços em branco
  # frozen=True gera automaticamente o método __init__, __eq__ e __hash__
  # garante imutabilidade da entidade Passageiro
  
  nome: str
  
  def __post_init__(self) -> None:
    # validação do nome do passageiro após a inicialização gerada pela dataclass
    if not self.nome or not self.nome.strip():
      raise ValueError("O nome do passageiro não pode ser vazio ou conter apenas espaços em branco.")
    
  def __str__(self) -> str:
    return f"Passageiro(nome='{self.nome}')"
    