# Import all server libraries
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import FileResponse
from pyramid.renderers import render_to_response

# Import all MySQL libraries
import mysql.connector as mysql
from dotenv import load_dotenv
import os

#import track
import coordinates

# Loads all details from the "credentials.env"
load_dotenv('Challenge/credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

# Home route
def index_page(req):
    path = 'Challenge/index.html'
    return FileResponse(path)

# Finds objects by panning to the center, once found get coordinates and send JSON
def get_object(req):
    object_name = str(req.matchdict['object_name'])

    # Track object (hardware code)
    #track.object_in_frame(object_name)

    # Get coordinates
    latitude, longitude = coordinates.locate()
    #city = coordinates.city()

    coordinate = str(latitude) + '°, ' + str(longitude) + '°'

    return {'coordinate': coordinate, 'city': 'empty_city'}

# Store object and its address in found_objects table
def record_address(req):
    object_name = str(req.matchdict['object_name'])
    coordinate = str(req.matchdict['coordinate'])

    # Connect to database
    db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
    cursor = db.cursor()

    # Find number of repeats
    cursor.execute("SELECT * FROM found_objects WHERE object_name LIKE '" + object_name + "%';")
    record = cursor.fetchall()
    object_id = len(record) + 1

    # New object name, given id
    object_name = object_name + "_" + str(object_id)

    # Store address into database
    query = "INSERT INTO found_objects (object_name, address) VALUES (%s, %s)"
    values = [(object_name, coordinate)]
    cursor.executemany(query, values)
    db.commit()
    db.close()

    return {'response': ''}

if __name__ == '__main__':

    with Configurator() as config:

        # Create a route called home, bind the view (defined by index_page) to the route named ‘home’
        config.add_route('home', '/')
        config.add_view(index_page, route_name='home')

        # Create a route called object, binds the function get_photo to the /{object} route and returns JSON
        config.add_route('object', '/object/{object_name}')
        config.add_view(get_object, route_name='object', renderer='json')

        # Create a route called record, binds the function get_photo to the /record/{object_name} route
        config.add_route('record', '/record/{object_name}/{coordinate}')
        config.add_view(record_address, route_name='record', renderer='json')

        # Add a static view
        config.add_static_view(name='/', path='./public', cache_max_age=3600)
         
        # Create an app with the configuration specified above
        app = config.make_wsgi_app()

    # Start the server on port 6543
    server = make_server('0.0.0.0', 6543, app) 
    server.serve_forever()