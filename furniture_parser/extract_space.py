import re
from furniture_parser.fuzzy_match import fuzzy_match
from furniture_parser.furniture_features import furniture_features

def extract_space(text: str) -> list[str]:
    """Extract the intended space (room) from the query text."""
    features_data = furniture_features()
    text_lower = text.lower()
        
    # Check for direct mentions of spaces
    for space, synonyms in features_data['spaces'].items():
        if space.lower() in text_lower:
            return space
            
        for synonym in synonyms:
            if synonym.lower() in text_lower:
                return space
        
    # Try fuzzy matching for space terms
    all_space_terms = []
    space_to_normalized = {}
        
    for space, synonyms in features_data['spaces'].items():
        all_space_terms.append(space.lower())
        space_to_normalized[space.lower()] = space
        for syn in synonyms:
            all_space_terms.append(syn.lower())
            space_to_normalized[syn.lower()] = space
        
    words = re.findall(r'\b\w+\b', text_lower)
    for word in words:
        matched_space = fuzzy_match(word, all_space_terms)
        if matched_space:
            return space_to_normalized.get(matched_space, matched_space)
        
    return None