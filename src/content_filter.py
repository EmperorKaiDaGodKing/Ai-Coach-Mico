"""
Content filter module: checks text for explicit content using keyword blacklist.
"""

import re
from typing import Tuple

# Compact blacklist of explicit sexual keywords/phrases (regex patterns)
BLACKLIST_PATTERNS = [
    r'\bsex\b',
    r'\bfuck',
    r'\bporn',
    r'\bnaked\b',
    r'\bnude\b',
    r'\bpenis\b',
    r'\bvagina\b',
    r'\bcock\b',
    r'\bpussy\b',
    r'\bcum\b',
    r'\borgasm',
    r'\bmasturbat',
    r'\berotic\s+roleplay',
    r'\bsexual\s+act',
    r'\bintercourse\b',
]

# Compile patterns for efficiency
BLACKLIST_REGEX = re.compile('|'.join(BLACKLIST_PATTERNS), re.IGNORECASE)


def check_safe(text: str) -> Tuple[bool, str]:
    """
    Check if the provided text is safe (does not contain blacklisted explicit content).
    
    Args:
        text: The text to check
        
    Returns:
        A tuple of (is_safe: bool, reason: str)
        - If safe: (True, "")
        - If unsafe: (False, "blacklist: <matched_keyword>")
    """
    if not text:
        return True, ""
    
    # Check against blacklist (regex already uses re.IGNORECASE)
    match = BLACKLIST_REGEX.search(text)
    if match:
        matched_word = match.group(0)
        return False, f"blacklist: {matched_word}"
    
    return True, ""
