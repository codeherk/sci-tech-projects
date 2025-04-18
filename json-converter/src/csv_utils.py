import csv
import io

def json_to_csv(json_data):
    """
    Converts JSON data to a CSV string.

    Args:
        json_data (list): A list of dictionaries representing the JSON data.

    Returns:
        str: A CSV string.
    """
    # Create a CSV file in memory
    csv_buffer = io.StringIO()
    csv_writer = csv.writer(csv_buffer)

    # Write the header row
    header = json_data[0].keys()
    csv_writer.writerow(header)

    # Write the data rows
    for record in json_data:
        csv_writer.writerow(record.values())

    # Return the CSV content as a string
    return csv_buffer.getvalue()