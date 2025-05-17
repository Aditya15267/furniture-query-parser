import json
from furniture_parser import parse_query

if __name__ == "__main__":
    # Example query
    query = "I am looking for a sofa with curvy back design, leather fabric, slanted legs and some metal design in it for under 30000 rupees in mumbai"
    result = parse_query(query)

    with open("query_result.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print("Query parsed and saved to query_result.json")