import pytest
from src.csv_utils import json_to_csv

def test_json_to_csv():
    # Sample JSON data
    json_data = [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 25, "city": "Los Angeles"}
    ]

    # Expected CSV output
    expected_csv = "name,age,city\r\nAlice,30,New York\r\nBob,25,Los Angeles\r\n"

    # Call the function
    csv_output = json_to_csv(json_data)

    # Assert the output matches the expected CSV
    assert csv_output == expected_csv