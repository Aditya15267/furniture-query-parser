from fuzzywuzzy import process

def fuzzy_match(term: str, choices: list[str], threshold: int = 75) -> list[str]:
    """Find a fuzzy match for a term within choices."""
    if not term or not choices:
        return None
        
    # Check for direct match first
    term_lower = term.lower()
    for choice in choices:
        if choice.lower() == term_lower:
            return choice
        
    # Try fuzzy matching
    matches = process.extractOne(term, choices)
    if matches and matches[1] >= threshold:
        return matches[0]
        
    return None
