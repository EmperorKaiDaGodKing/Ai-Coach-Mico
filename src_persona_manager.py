"""
Root-level src_persona_manager module for backward compatibility.
This is a simple wrapper that delegates to src.persona_manager.
"""
from src.persona_manager import PersonaManager

__all__ = ['PersonaManager']
