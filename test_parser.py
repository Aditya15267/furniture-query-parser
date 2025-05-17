import unittest
from parser import parse_query

class TestParseQuery(unittest.TestCase):
    def setUp(self):
        pass

    def test_parse_query(self):
        query = "I am looking for a sofa with curvy back design, leather fabric, slanted legs and some metal design in it for under 30000 rupees in mumbai"

        expected_output = {
            "product_type": "Sofa",
            "features": {
                "Back": [ "Curved Back" ],
                "Upholstery": [ "Leather", "Fabric" ],
                "Legs": [ "Inclined Leg", "Metal Detail", "Inclined Leg" ],
                "Structure": [ "Metal", "Metal detail" ],
                "Material": [ "Metal" ]
            },
            "price_range": {
                "min": None,
                "max": 30000,
                "currency": "INR"
            },
            "location": "Mumbai",
            "space": "Office"
        }

        result = parse_query(query)
        self.assertEqual(result, expected_output)

    def test_misspellings(self):
        query = "Looking for a leathr sofa with curvy back for my living room"
        result = parse_query(query)
        self.assertIn("Sofa", result["product_type"])
        self.assertIn("Leather", result["features"]["Upholstery"])
        self.assertIn("Curved Back", result["features"]["Back"])
        self.assertIn("Living Room", result["space"])

    def test_price_range(self):
        query = "I need a table between 15000-25000 rupees"
        result = parse_query(query)
        self.assertEqual(result["price_range"]["min"], 15000)
        self.assertEqual(result["price_range"]["max"], 25000)
        self.assertEqual(result["price_range"]["currency"], "INR")

        query = "I need a table under 15000 rupees"
        result = parse_query(query)
        self.assertEqual(result["price_range"]["min"], None)
        self.assertEqual(result["price_range"]["max"], 15000)
        self.assertEqual(result["price_range"]["currency"], "INR")

        query = "I need a table with min 15000 rupees"
        result = parse_query(query)
        self.assertEqual(result["price_range"]["min"], 15000)
        self.assertEqual(result["price_range"]["max"], None)
        self.assertEqual(result["price_range"]["currency"], "INR")

    def test_different_currencies(self):
        query = "I need a table under $15000"
        result = parse_query(query)
        self.assertEqual(result["price_range"]["min"], None)
        self.assertEqual(result["price_range"]["max"], 15000)
        self.assertEqual(result["price_range"]["currency"], "USD")

        query = "I need a sofa above 1500 euros"
        result = parse_query(query)
        self.assertEqual(result["price_range"]["min"], 1500)
        self.assertEqual(result["price_range"]["max"], None)
        self.assertEqual(result["price_range"]["currency"], "EUR")

    def test_different_product_types(self):
        product_types = [
            ("I need a new couch", "Sofa"),
            ("Looking for a comfortable chair", "Chair"),
            ("Need a sturdy table", "Table"),
            ("Shopping for a queen bed", "Bed"),
            ("I want a large wardrobe", "Wardrobe"),
            ("Need a bookcase for my books", "Bookshelf"),
            ("Looking for a cabinet with storage", "Cabinet")
        ]
        
        for query, expected_type in product_types:
            result = parse_query(query)
            self.assertEqual(result["product_type"], expected_type)
    
    def test_locations(self):
        query = "Need a sofa in bangalore"
        result = parse_query(query)
        self.assertEqual(result["location"], "Bangalore")
        
        query = "Looking for furniture in new delhi"
        result = parse_query(query)
        self.assertEqual(result["location"], "Delhi")
    
    def test_spaces(self):
        spaces = [
            ("Need a sofa for my living area", "Living Room"),
            ("Looking for a bed for the master bedroom", "Bedroom"),
            ("Need a desk for home office", "Office"),
            ("Want a table for dining area", "Dining Room"),
            ("Looking for chairs for the balcony", "Balcony"),
            ("Need furniture for kids room", "Children's Room")
        ]
        
        for query, expected_space in spaces:
            result = parse_query(query)
            self.assertEqual(result["space"], expected_space)
    
    def test_complex_query(self):
        query = "I'm looking for a wooden dining table with glass top, metal legs, rectangular shape, for my dining room in pune, budget between 20000 and 35000 rupees"
        result = parse_query(query)
        
        self.assertEqual(result["product_type"], "Table")
        self.assertIn("Wood", result["features"]["Material"])
        self.assertIn("Glass", result["features"]["Material"])
        self.assertEqual(result["price_range"]["min"], 20000)
        self.assertEqual(result["price_range"]["max"], 35000)
        self.assertEqual(result["location"], "Pune")
        self.assertEqual(result["space"], "Dining Room")
    
    def test_missing_fields(self):
        query = "I just want a nice chair"
        result = parse_query(query)
        
        self.assertEqual(result["product_type"], "Chair")
        self.assertIsNone(result.get("location"))
        self.assertEqual(result["price_range"]["min"], None)
        self.assertEqual(result["price_range"]["max"], None)

if __name__ == "__main__":
    unittest.main()