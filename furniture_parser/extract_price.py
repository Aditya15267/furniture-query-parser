import re
from furniture_parser.furniture_features import furniture_features

def extract_price_range(text: str) -> dict[str, any]:
    """Extract the price range from the query text."""
    price_range = {"min": None, "max": None, "currency": None}
        
    # Determine currency
    currency = extract_currency(text)
    if currency:
        price_range["currency"] = currency
        
    # Pattern for price ranges: X-Y, X to Y, between X and Y
    range_patterns = [
        r'(\d+[\d,.]*)\s*[-–—to]\s*(\d+[\d,.]*)',  # X-Y or X to Y
        r'between\s+(\d+[\d,.]*)\s+and\s+(\d+[\d,.]*)'  # between X and Y
    ]
        
    for pattern in range_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            min_price = match.group(1).replace(',', '').replace('.', '')
            max_price = match.group(2).replace(',', '').replace('.', '')
            price_range["min"] = int(min_price)
            price_range["max"] = int(max_price)
            return price_range
        
    # Pattern for maximum price: under X, less than X, max X, below X, up to X
    max_patterns = [
        r'(?:under|less than|max|maximum|below|up to|not more than)\s+(?:\D*)(\d+[\d,.]*)',
        r'(?:below|under|within|cheaper than|lesser than)\s+(?:\D*)(\d+[\d,.]*)'
    ]
        
    for pattern in max_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            max_price = match.group(1).replace(',', '').replace('.', '')
            price_range["max"] = int(max_price)
            return price_range
        
    # Pattern for minimum price: over X, more than X, min X, above X, at least X
    min_patterns = [
        r'(?:over|more than|min|minimum|above|at least|starting from)\s+(?:\D*)(\d+[\d,.]*)',
        r'(?:above|over|exceeding|starting at|from)\s+(?:\D*)(\d+[\d,.]*)'
    ]
        
    for pattern in min_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            min_price = match.group(1).replace(',', '').replace('.', '')
            price_range["min"] = int(min_price)
            return price_range
        
    # Look for a standalone price number
    price_pattern = r'(?:₹|\$|€|£|rs\.?|rupees?|inr|usd|eur|gbp)?\s*(\d+[\d,.]*)'
    match = re.search(price_pattern, text, re.IGNORECASE)
    if match:
        price = match.group(1).replace(',', '').replace('.', '')
        price_range["max"] = int(price)
        
    return price_range

def extract_currency(text: str) -> str:
    """Extract the currency from the text."""
    features_data = furniture_features()
    text_lower = text.lower()
        
    for currency, symbols in features_data['currencies'].items():
        for symbol in symbols:
            if symbol.lower() in text_lower:
                return currency
        
    # Default to INR if no currency specified
    return "INR"