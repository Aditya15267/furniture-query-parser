import re
from furniture_parser.furniture_features import furniture_features
from fuzzywuzzy import fuzz


def extract_product_type(text: str) -> str:
    """Extract the product type from the query text."""
    features_data = furniture_features()

    # Create a flat list of all product types with their synonyms
    all_product_terms = []
    product_to_normalized = {}
        
    for product, synonyms in features_data['product_types'].items():
        all_product_terms.append(product.lower())
        product_to_normalized[product.lower()] = product
        for syn in synonyms:
            all_product_terms.append(syn.lower())
            product_to_normalized[syn.lower()] = product
        
    # Extract words from text and check for product type
    words = [w.lower() for w in re.findall(r'\b\w+\b', text)]
        
    # Check for exact matches
    for word in words:
        if word in all_product_terms:
            return product_to_normalized[word]
        
        # If no exact match, try fuzzy matching
        for word in words:
            for product_term in all_product_terms:
                if fuzz.ratio(word, product_term) > 80:
                    return product_to_normalized[product_term]
        
        # If no match found, default to "Unknown"
        return "Unknown"