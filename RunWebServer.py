import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading
import time

class MyHandler(SimpleHTTPRequestHandler):
    last_heartbeat = time.time()
    
    def do_GET(self):
        if self.path == '/heartbeat':
            self.send_response(200)
            self.end_headers()
            MyHandler.last_heartbeat = time.time()
        else:
            super().do_GET()

    @classmethod
    def check_heartbeat(cls):
        while True:
            time.sleep(10)  # Check every 10 seconds
            if time.time() - cls.last_heartbeat > 15:  # 15 seconds without heartbeat
                print("No heartbeat detected, shutting down.")
                server.shutdown()
                break

port = 8000
server = HTTPServer(('', port), MyHandler)
threading.Thread(target=MyHandler.check_heartbeat).start()
webbrowser.open_new_tab(f'http://localhost:{port}/index.html')
server.serve_forever()
