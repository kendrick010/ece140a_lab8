# # Import all server libraries
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import FileResponse
from pyramid.renderers import render_to_response

# Import all MySQL libraries
import mysql.connector as mysql
from dotenv import load_dotenv
import os

# Loads all details from the "credentials.env"
load_dotenv('Challenge/credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

def index_page(req):
    path = 'Challenge/index.html'
    return FileResponse(path)

if __name__ == '__main__':

    with Configurator() as config:

        # Create a route called home, bind the view (defined by index_page) to the route named ‘home’
        config.add_route('home', '/')
        config.add_view(index_page, route_name='home')

        # Add a static view
        config.add_static_view(name='/', path='./public', cache_max_age=3600)
         
        # Create an app with the configuration specified above
        app = config.make_wsgi_app()

    # Start the server on port 6543
    server = make_server('0.0.0.0', 6543, app) 
    server.serve_forever()