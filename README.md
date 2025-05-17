# Query Parser

This project implements a context aware parser that extracts structured information from unstructured queries. It handles synonyms, misspellings, and extracts product types, features, price ranges, locations and intended spaces.

## Features

- Extracts product type (sofa,chair, table, etc.)
- Identifies product features categorized by Back, Upholstery, Legs, Structure, etc.
- Parses price ranges with support for different formats and currencies
- Handles spelling errors and synonyms
- Extract location information
- Identifies intended space/room

## Prerequisites

- Python 3.6+
- Dependencies: fuzzywuzzy

## Setup

1. Clone this repository:
    ```sh
    git clone https://github.com/Aditya15267/furniture-query-parser.git
    cd furniture-query-parse
    ```

2. Install the dependencies
    ```sh
    pip install -r requirements.txt
    ```

## Approach

The parser uses a hybrid approach combining:

1. **Regular expressions** for price extraction and pattern matching
2. **Fuzzy matching** for handling misspellings and variations 
3. **Synonym dictionaries** for normalizing terms
4. **Rule-based extractions** for identifying product types and features

## Key Components

- **Product Type Identification:** Matches against a dictionary of furniture types and their synonyms
- **Feature Extraction:** Categories features into Back, Upholstery, Legs, Structure, etc.
- **Spelling Correction:** Uses fuzzy matching and common misspelling dictionary
- **Location Extraction:** Identifies city names in the query
- **Space Identification:** Detects intended space/room (Living room, bedroom, etc.)

## Testing

Run the test suite to verify parser functionality:

```py
python test_parser.py
```

The test suite includes diverse examples covering different product types, features, price formats, and handling of misspellings and synonyms.


