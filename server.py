import http.server
import socketserver
import os
import re
import json

def create_index(dir):
    """
    Creates an index of the words in the files in the given directory and its subfolders,
    along with short descriptions.
    """
    index = {}
    for root, _, files in os.walk(dir):
        for filename in files:
            if filename.endswith((".txt", ".png", ".jpg", ".jpeg")):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r') as f:
                        if filename.endswith(".txt"):
                            text = f.read()
                            words = re.findall(r'\b\w+\b', text.lower())
                            for word in words:
                                if word not in index:
                                    index[word] = []
                                description = text[:text.find('.') + 1]
                                index[word].append((filename, description))
                        else:
                            if filename not in index:
                                index[filename] = []
                            index[filename].append((filename, "Image file"))
                except Exception as e:
                    print(f"Error processing file {filename}: {e}")
    return index

def search(index, query):
    """
    Searches the index for the given query.
    """
    query = query.lower()
    results = []
    for word, filenames in index.items():
        if word in query:
            results.extend(filenames)
    return list(set(results))

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        filepath = None

        if self.path.startswith('/search'):
            try:
                # Parse query parameters using urllib.parse
                query_params = urllib.parse.urlparse(self.path).query
                query = urllib.parse.parse_qs(query_params).get('q', [''])[0]  # Extract 'q' parameter

                index = create_index(r'C:\Users\nicholas.nesmith0001\Documents\Search Engine')
                results = search(index, query)

                formatted_results = []
                for filename, description in results:
                    filepath = find_file_in_subfolders(filename, r'C:\Users\nicholas.nesmith0001\Documents\Search Engine')
                    if filepath:
                        formatted_results.append({
                            'filename': filename,
                            'description': description,
                            'filepath': filepath
                        })

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'results': formatted_results}).encode())

            except Exception as e:
                print(f"Error processing request: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'An error occurred'}).encode())

        # Explicitly handle requests for static files
        elif self.path == '/search.html':
            filepath = 'search.html'
        elif self.path == '/style.css':
            filepath = 'style.css'
        elif self.path == '/script.js':
            filepath = 'script.js'

        if filepath:
            try:
                with open(filepath, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                if filepath.endswith('.html'):
                    self.send_header('Content-type', 'text/html')
                elif filepath.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif filepath.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript')
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'File not found')
            except Exception as e:
                print(f"Error serving static file: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'Internal server error')
        else:
            super().do_GET()  # Serve other files as usual


def find_file_in_subfolders(filename, root_dir):
    """
    Helper function to find the full path of a file within subfolders.
    """
    for root, _, files in os.walk(root_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None

PORT = 8000
Handler = Handler
httpd = socketserver.TCPServer(("", PORT), Handler)
print(f"Serving at port {PORT}")
httpd.serve_forever()