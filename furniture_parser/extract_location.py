import re
import string
from furniture_parser.fuzzy_match import fuzzy_match

def extract_location(text: str) -> list[str]:
    """Extract location from the query text."""
    # List of common Indian cities
    cities = ["mumbai", "delhi", "bangalore", "kolkata", "chennai", "hyderabad", 
                "pune", "ahmedabad", "jaipur", "lucknow", "kanpur", "nagpur", 
                "indore", "thane", "bhopal", "visakhapatnam", "surat", "agra"]
        
    text_lower = text.lower()
        
    # Check for direct mentions of cities
    for city in cities:
        if city in text_lower:
            return string.capwords(city)
        
    # Try fuzzy matching for misspelled city names
    words = re.findall(r'\b\w+\b', text_lower)
    for word in words:
        if len(word) > 3:  # Only consider words of reasonable length
            matched_city = fuzzy_match(word, cities)
            if matched_city:
                return string.capwords(matched_city)
        
    return None