from parser import parse_query


def compute_per_field_metrics(test_cases):
    """Compute precision and recall for features and price extraction."""
    
    # Initialize counters for features
    feature_true_positives = 0
    feature_false_positives = 0
    feature_false_negatives = 0
    
    # Initialize counters for price range
    price_correct = 0
    price_incorrect = 0
    price_missing = 0
    
    # Initialize counters for location and space
    location_correct = 0
    location_incorrect = 0
    location_missing = 0
    space_correct = 0
    space_incorrect = 0
    space_missing = 0
    
    for query, expected in test_cases:
        result = parse_query(query)
        
        # Evaluate features
        expected_features = expected.get("features", {})
        result_features = result.get("features", {})
        
        # For each category in expected features
        for category, values in expected_features.items():
            if category in result_features:
                result_values = result_features[category]
                
                # Count matches
                for value in values:
                    if value in result_values:
                        feature_true_positives += 1
                    else:
                        feature_false_negatives += 1
                
                # Count false positives
                for value in result_values:
                    if value not in values:
                        feature_false_positives += 1
            else:
                # Category missing in results
                feature_false_negatives += len(values)
        
        # For each category in result features but not in expected
        for category, values in result_features.items():
            if category not in expected_features:
                feature_false_positives += len(values)
        
        # Evaluate price range
        expected_price = expected.get("price_range", {})
        result_price = result.get("price_range", {})
        
        if expected_price and result_price:
            if (expected_price.get("min") == result_price.get("min") and
                expected_price.get("max") == result_price.get("max") and
                expected_price.get("currency") == result_price.get("currency")):
                price_correct += 1
            else:
                price_incorrect += 1
        elif expected_price and not result_price:
            price_missing += 1
        elif not expected_price and result_price:
            price_incorrect += 1
        
        # Evaluate location
        expected_location = expected.get("location")
        result_location = result.get("location")
        
        if expected_location and result_location:
            if expected_location == result_location:
                location_correct += 1
            else:
                location_incorrect += 1
        elif expected_location and not result_location:
            location_missing += 1
        elif not expected_location and result_location:
            location_incorrect += 1
        
        # Evaluate space
        expected_space = expected.get("space")
        result_space = result.get("space")
        
        if expected_space and result_space:
            if expected_space == result_space:
                space_correct += 1
            else:
                space_incorrect += 1
        elif expected_space and not result_space:
            space_missing += 1
        elif not expected_space and result_space:
            space_incorrect += 1
    
    # Calculate precision and recall for features
    if feature_true_positives + feature_false_positives > 0:
        feature_precision = feature_true_positives / (feature_true_positives + feature_false_positives)
    else:
        feature_precision = 0
        
    if feature_true_positives + feature_false_negatives > 0:
        feature_recall = feature_true_positives / (feature_true_positives + feature_false_negatives)
    else:
        feature_recall = 0
    
    feature_f1 = 0
    if feature_precision + feature_recall > 0:
        feature_f1 = 2 * (feature_precision * feature_recall) / (feature_precision + feature_recall)
    
    # Calculate accuracy for price range
    price_total = price_correct + price_incorrect + price_missing
    price_accuracy = price_correct / price_total if price_total > 0 else 0
    
    # Calculate accuracy for location
    location_total = location_correct + location_incorrect + location_missing
    location_accuracy = location_correct / location_total if location_total > 0 else 0
    
    # Calculate accuracy for space
    space_total = space_correct + space_incorrect + space_missing
    space_accuracy = space_correct / space_total if space_total > 0 else 0
    
    print("\nPer-field metrics:")
    print("\nFeatures:")
    print(f"  Precision: {feature_precision:.2f}")
    print(f"  Recall: {feature_recall:.2f}")
    print(f"  F1 Score: {feature_f1:.2f}")
    
    print("\nPrice Range:")
    print(f"  Accuracy: {price_accuracy:.2f}")
    
    print("\nLocation:")
    print(f"  Accuracy: {location_accuracy:.2f}")
    
    print("\nSpace:")
    print(f"  Accuracy: {space_accuracy:.2f}")
    
    return {
        "features": {
            "precision": feature_precision,
            "recall": feature_recall,
            "f1": feature_f1
        },
        "price": {
            "accuracy": price_accuracy
        },
        "location": {
            "accuracy": location_accuracy
        },
        "space": {
            "accuracy": space_accuracy
        }
    }

def main():
    # Define test cases as (query, expected_output) pairs
    test_cases = [
        # Test case 1: Original example from assignment
        (
            "I am looking for a sofa with curvy back design, leather fabric, slanted legs and some metal design in it for under 30000 rupees in mumbai",
            {
                "product_type": "Sofa",
                "features": {
                    "Back": ["Curved Back"],
                    "Upholstery": ["Leather"],
                    "Legs": ["Inclined Leg", "Metal Detail"],
                    "Structure": ["Metal detail"]
                },
                "price_range": {
                    "min": None,
                    "max": 30000,
                    "currency": "INR"
                },
                "location": "Mumbai",
                "space": None
            }
        ),
        # Test case 2: Different product with misspellings
        (
            "Need a sturdy woden table with glas top for my dining area in bangalore",
            {
                "product_type": "Table",
                "features": {
                    "Material": ["Wood", "Glass"]
                },
                "price_range": {
                    "min": None,
                    "max": None,
                    "currency": "INR"
                },
                "location": "Bangalore",
                "space": "Dining Room"
            }
        ),
        # Test case 3: Price range with different format
        (
            "Looking for a chair in the range of 5000-10000 rs for my home office",
            {
                "product_type": "Chair",
                "features": {},
                "price_range": {
                    "min": 5000,
                    "max": 10000,
                    "currency": "INR"
                },
                "location": None,
                "space": "Office"
            }
        ),
        # Test case 4: Different currency
        (
            "I want to buy a bookshelf under $300 for my study room",
            {
                "product_type": "Bookshelf",
                "features": {},
                "price_range": {
                    "min": None,
                    "max": 300,
                    "currency": "USD"
                },
                "location": None,
                "space": "Office"
            }
        ),
        # Test case 5: Complex query with multiple features
        (
            "Looking for a queen-sized bed with wooden frame, storage drawers underneath, for my master bedroom in pune, budget between 20000 and 40000",
            {
                "product_type": "Bed",
                "features": {
                    "Material": ["Wood"],
                    "Structure": ["Wooden frame"]
                },
                "price_range": {
                    "min": 20000,
                    "max": 40000,
                    "currency": "INR"
                },
                "location": "Pune",
                "space": "Bedroom"
            }
        ),
        # Test case 6: Minimal query
        (
            "I just want a nice chair",
            {
                "product_type": "Chair",
                "features": {},
                "price_range": {
                    "min": None,
                    "max": None,
                    "currency": "INR"
                },
                "location": None,
                "space": None
            }
        ),
        # Test case 7: Query with synonyms
        (
            "Need a couch with wavy back and leathr upholstery for my lounge",
            {
                "product_type": "Sofa",
                "features": {
                    "Back": ["Curved Back"],
                    "Upholstery": ["Leather"]
                },
                "price_range": {
                    "min": None,
                    "max": None,
                    "currency": "INR"
                },
                "location": None,
                "space": "Living Room"
            }
        ),
        # Test case 8: Different price format
        (
            "Need a wardrobe below ₹25k for my bedroom in delhi",
            {
                "product_type": "Wardrobe",
                "features": {},
                "price_range": {
                    "min": None,
                    "max": 25000,
                    "currency": "INR"
                },
                "location": "Delhi",
                "space": "Bedroom"
            }
        ),
        # Test case 9: Multiple spaces and features
        (
            "I'm looking for a cabinet with metal frame and glass doors for my kitchen and dining area",
            {
                "product_type": "Cabinet",
                "features": {
                    "Structure": ["Metal"],
                    "Material": ["Glass"]
                },
                "price_range": {
                    "min": None,
                    "max": None,
                    "currency": "INR"
                },
                "location": None,
                "space": "Dining Room"
            }
        ),
        # Test case 10: Query with different price expression
        (
            "Need a desk for max 15000 rupees with metal legs and wooden top for my workspace",
            {
                "product_type": "Table",
                "features": {
                    "Legs": ["Metal Leg"],
                    "Material": ["Wood"]
                },
                "price_range": {
                    "min": None,
                    "max": 15000,
                    "currency": "INR"
                },
                "location": None,
                "space": "Office"
            }
        )
    ]
    
    print("Evaluating Furniture Query Parser...")
    print("=" * 50)
    
    print("\n" + "=" * 50)
    
    # Compute per-field metrics
    metrics = compute_per_field_metrics(test_cases)
    
    # Output summary
    print("\nSummary:")
    print(f"Feature F1 Score: {metrics['features']['f1']:.2f}")
    print(f"Price Accuracy: {metrics['price']['accuracy']:.2f}")
    print(f"Location Accuracy: {metrics['location']['accuracy']:.2f}")
    print(f"Space Accuracy: {metrics['space']['accuracy']:.2f}")

if __name__ == "__main__":
    main()