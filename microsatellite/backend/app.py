from flask import Flask, jsonify, make_response
from flask_cors import CORS
import mysql.connector
import os
import logging

# Create a Flask app
app = Flask(__name__)
CORS(app)

# Get environment variables
host = os.getenv("MYSQL_HOST")
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
database = os.getenv("MYSQL_DATABASE")

# Define a route for the microsatellite API
@app.route('/microsatellites')
def get_microsatellites():
    try:
        # Set up a MySQL connection
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Execute a SELECT query to retrieve all microsatellites from the database
        cursor.execute("SELECT * FROM microsatellites")

        # Fetch all rows as a list of tuples
        rows = cursor.fetchall()

        # Create an empty list to store the microsatellites as dictionaries
        microsatellites = []

        # For each row in the results
        for row in rows:
            # Create a dictionary for the microsatellite data
            microsatellite = {
                "id": row[0],
                "name": row[1],
                "base": row[2],
                "repeats": row[3]
            }

            # Add the dictionary to the list of microsatellites
            microsatellites.append(microsatellite)

        cursor.close() 
        # Return the list of microsatellites as JSON
        response = jsonify(microsatellites)
        response.status_code = 200
        return response

    except Exception as err:
        print(err)
        message = jsonify(message='Internal Server Error')
        return make_response(message, 500)
    finally: 
        conn.close()  


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
    logging.info("Now running Microsatllites API")
