"""
Root-level content_filter module for backward compatibility.
This is a simple wrapper that delegates to src.content_filter.
"""
from src.content_filter import check_safe

__all__ = ['check_safe']
