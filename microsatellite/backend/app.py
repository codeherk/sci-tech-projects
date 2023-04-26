from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import mysql.connector
import os
import logging

select_microsatellites_statement = 'SELECT * FROM microsatellites'
insert_microsatellites_statement = ('INSERT INTO microsatellites '
               '(name, base, repeats) '
               'VALUES (%s, %s, %s)')

# Create a Flask app
app = Flask(__name__)
CORS(app)

logger = logging.getLogger('werkzeug')
logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler('app.log')
# logger.addHandler(handler)

# Get environment variables
host = os.getenv('MYSQL_HOST')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
database = os.getenv('MYSQL_DATABASE')

# Define a route for the microsatellite API
@app.route('/microsatellites', methods = ['GET'])
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
        logger.info('Fetching data from Microsatellites table.')

        # Execute a SELECT query to retrieve all microsatellites from the database
        cursor.execute(select_microsatellites_statement)

        # Fetch all rows as a list of tuples
        rows = cursor.fetchall()

        # Create an empty list to store the microsatellites as dictionaries
        microsatellites = []

        # For each row in the results
        for row in rows:
            # Create a dictionary for the microsatellite data
            microsatellite = {
                'id': row[0],
                'name': row[1],
                'base': row[2],
                'repeats': row[3]
            }

            # Add the dictionary to the list of microsatellites
            microsatellites.append(microsatellite)

        cursor.close()
        conn.close()  

        logger.info('Fetch successful.')

        # Return the list of microsatellites as JSON
        response = jsonify(microsatellites)
        response.status_code = 200
        return response
    except Exception as err:
        print(err)
        message = jsonify(message='Internal Server Error')
        return make_response(message, 500)


@app.route('/microsatellites', methods = ['POST'])
def post_microsatellites():
    try:
        data = request.get_json()

        name = data.get('name', '')
        base = data.get('base', '')
        repeats = data.get('repeats', '')

        if name == '' or repeats == '' or name == '':
            logger.info('Invalid request. All values for microsatellite were not provided.')
            message = jsonify(message='Bad Request')
            return make_response(message, 400)
        # Set up a MySQL connection
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        logger.info('Inserting data into Microsatellites table.')

        # Execute a SELECT query to retrieve all microsatellites from the database
        cursor.execute(insert_microsatellites_statement, (name,base,repeats))

        # Make sure data is committed to the database
        conn.commit()
        
        cursor.close()
        conn.close()

        logger.info('Insertion successful.')
        # Return success
        return ('', 200)

    except Exception as err:
        print(err)
        message = jsonify(message='Internal Server Error.')
        return make_response(message, 500) 

@app.before_request
def log_request_info():
    logger.debug('Headers: %s', request.headers)
    logger.debug('Body: %s', request.get_data())

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
    logger.info('Now running Microsatellites API.')
