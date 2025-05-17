def furniture_features():
    """
    This function returns a dictionary of features and their synonyms for furniture items.
    
    Returns:
        dict: A dictionary where keys are feature categories and values are dictionaries.
    """
    # Dictionary of product types and their synonyms
    product_types = {
        "Sofa": ["couch", "settee", "loveseat", "divan", "futon"],
        "Chair": ["armchair", "recliner", "seat", "stool"],
        "Table": ["desk", "coffee table", "side table", "dining table", "console"],
        "Bed": ["cot", "bunk", "mattress", "bedstead"],
        "Wardrobe": ["cupboard", "closet", "armoire", "almirah"],
        "Bookshelf": ["bookcase", "shelves", "shelf unit", "book rack"],
        "Cabinet": ["chest", "bureau", "dresser", "sideboard", "credenza"]
    }
        
    # Dictionary of feature categories and their possible values
    feature_categories = {
        "Back": ["curved back", "straight back", "high back", "low back", "wavy back"],
        "Upholstery": ["leather", "fabric", "velvet", "cotton", "linen", "polyester", "suede", "wool"],
        "Legs": ["straight leg", "tapered leg", "curved leg", "inclined leg", "metal leg", "wooden leg", "folding leg"],
        "Structure": ["metal", "wood", "plastic", "glass", "metal detail", "wooden frame"],
        "Color": ["black", "white", "brown", "beige", "gray", "red", "blue", "green", "yellow"],
        "Material": ["solid wood", "engineered wood", "plywood", "mdf", "particleboard", "metal", "glass", "plastic", "wood"]
    }
        
    # Dictionary of spaces and their synonyms
    spaces = {
        "Living Room": ["living area", "lounge", "sitting room", "family room", "drawing room"],
        "Bedroom": ["bed room", "master bedroom", "guest room"],
        "Office": ["study room", "workspace", "home office", "study", "work area"],
        "Dining Room": ["dining area", "kitchen", "breakfast area"],
        "Balcony": ["terrace", "patio", "outdoor space"],
        "Children's Room": ["kids room", "nursery", "playroom"]
    }
        
    # Currencies and their symbols
    currencies = {
        "INR": ["₹", "rs", "rs.", "rupee", "rupees", "inr"],
        "USD": ["$", "dollar", "dollars", "usd"],
        "EUR": ["€", "euro", "euros", "eur"],
        "GBP": ["£", "pound", "pounds", "gbp"]
    }
        
    # Common misspellings
    common_misspellings = {
        "curvy": "curved",
        "leathr": "leather",
        "metl": "metal",
        "plastc": "plastic",
        "woden": "wooden",
        "glas": "glass",
        "fabrc": "fabric",
        "wavy": "curved",
        "slanted": "inclined"
    }

    return {
        "product_types": product_types,
        "feature_categories": feature_categories,
        "spaces": spaces,
        "currencies": currencies,
        "common_misspellings": common_misspellings
    }