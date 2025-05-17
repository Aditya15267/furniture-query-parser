import re
import string
from furniture_parser.furniture_features import furniture_features

def extract_features(text: str) -> dict[str, list[str]]:
    """Extract features from the query text."""
    features_data = furniture_features()
    features = {}
        
    # Preprocess text
    text_lower = text.lower()
        
    # Apply common misspelling corrections
    for misspelled, correct in features_data['common_misspellings'].items():
        text_lower = re.sub(r'\b' + misspelled + r'\b', correct, text_lower)
        
    # Extract features by category
    for category, values in features_data['feature_categories'].items():
        matched_values = []
            
        for value in values:
            value_lower = value.lower()
                
            # Check for direct matches
            if value_lower in text_lower:
                matched_values.append(normalize_feature_value(value, category))
                continue
                
            # Check for partial matches (e.g., "leather" instead of "leather upholstery")
            value_parts = value_lower.split()
            if any(part in text_lower for part in value_parts) and len(value_parts) == 1:
                # For single word values like "leather", "metal", etc.
                if value_lower in text_lower:
                    matched_values.append(normalize_feature_value(value, category))
                
            # Handle compound features like "curved back" or "metal legs"
            if category == "Back" and ("curved" in text_lower or "curvy" in text_lower or "wavy" in text_lower) and ("back" in text_lower):
                if "Curved Back" not in matched_values:
                    matched_values.append("Curved Back")
                
            if category == "Legs" and ("slanted" in text_lower or "inclined" in text_lower) and ("leg" in text_lower or "legs" in text_lower):
                if "Inclined Leg" not in matched_values:
                    matched_values.append("Inclined Leg")
                
            if category == "Structure" and "metal" in text_lower and "design" in text_lower:
                if "Metal detail" not in matched_values:
                    matched_values.append("Metal detail")
                
            if category == "Legs" and "metal" in text_lower and ("leg" in text_lower or "legs" in text_lower):
                if "Metal Detail" not in matched_values:
                    matched_values.append("Metal Detail")
            
        if matched_values:
            features[category] = matched_values
        
    return features

def normalize_feature_value(value: str, category: str) -> str:
    """Normalize feature values to title case, with special handling for some categories."""
    normalized = string.capwords(value)
        
    # Special handling for certain feature categories
    if category == "Back" and "Back" not in normalized:
        normalized += " Back"
    elif category == "Legs" and "Leg" not in normalized:
        normalized += " Leg"
        
    return normalized