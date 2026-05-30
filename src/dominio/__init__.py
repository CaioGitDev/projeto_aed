"""Entidades do domínio do Sistema de Gestão de Linha de Autocarros."""
 
from .passageiro import Passageiro
from .paragem import Paragem
from .autocarro import Autocarro
from .linha import Linha
 
__all__ = ["Passageiro", "Paragem", "Autocarro", 'Linha']