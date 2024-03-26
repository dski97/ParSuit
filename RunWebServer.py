import os
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Set the port number for the web server
port = 8000

# Change the working directory to the current directory
os.chdir(current_dir)

# Start the web server
server_address = ('', port)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
print(f"Server running on http://localhost:{port}")

# Open index.html in the default web browser
webbrowser.open_new_tab(f"http://localhost:{port}/index.html")

# Serve requests indefinitely
httpd.serve_forever()