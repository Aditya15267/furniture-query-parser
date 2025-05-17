from furniture_parser.extract_feature import extract_features
from furniture_parser.extract_product import extract_product_type
from furniture_parser.extract_price import extract_price_range
from furniture_parser.extract_location import extract_location
from furniture_parser.extract_space import extract_space

def parse_query(text: str) -> dict[str, any]:
    """Parse the user query and return a structured representation."""
    result = {
        "product_type": extract_product_type(text),
        "features": extract_features(text),
        "price_range": extract_price_range(text),
    }
        
    # Extract location if present
    location = extract_location(text)
    if location:
        result["location"] = location
        
    # Extract space if present
    space = extract_space(text)
    if space:
        result["space"] = space
        
    return result