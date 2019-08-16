"""
Important : Doesn't work at the moment, will fix when I have time.

"""

import errno
import os
import signal
import socket
import sys
import io

"""

Deals with the problems in load balancing of server by incorporating
- Simultaneous requests
- Zombie processes
- Orphan processes

"""
class WSGIServer(object):
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 1

    def __init__(server_address):
        # Create a listening socket
        WSGIServer.listen_socket = listen_socket = socket.socket(WSGIServer.address_family,WSGIServer.socket_type)
        # Allow to reuse the same address
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind
        listen_socket.bind(server_address)
        # Activate
        listen_socket.listen(WSGIServer.request_queue_size)
        # Get server host name and port
        host, port = WSGIServer.listen_socket.getsockname()[:2]
        WSGIServer.server_name = socket.getfqdn(host)
        WSGIServer.server_port = port
        # Return headers set by Web framework/Web application
        WSGIServer.headers_set = []

    def set_app(WSGIServer, application):
        WSGIServer.application = application

    def serve_forever(WSGIServer):
        listen_socket = WSGIServer.listen_socket
        while True:
            try:
                client_connection, client_address = listen_socket.accept()
            except IOError as e:
                code, msg = e.args
                # restart 'accept' if it was interrupted
                if code == errno.EINTR:
                    continue
                else:
                    raise

            pid = os.fork()
            if pid == 0:  # child
                listen_socket.close()  # close child copy
                handle_one_request(client_connection)
                client_connection.close()
                os._exit(0)
            else:  # parent
                client_connection.close()  # close parent copy and loop over

            signal.signal(signal.SIGCHLD, grim_reaper)


    def parse_request(text):
        request_line = text.splitlines()[0]
        request_line = request_line.rstrip('\r\n')
        # Break down the request line into components
        (WSGIServer.request_method,  # GET
         WSGIServer.path,            # /hello
         WSGIServer.request_version  # HTTP/1.1
         ) = request_line.split()

    def get_environ():
        env = {}
        # The following code snippet does not follow PEP8 conventions
        # but it's formatted the way it is for demonstration purposes
        # to emphasize the required variables and their values
        #
        # Required WSGI variables
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = io.StringIO(WSGIServer.request_data)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        # Required CGI variables
        env['REQUEST_METHOD']    = WSGIServer.request_method    # GET
        env['PATH_INFO']         = WSGIServer.path              # /hello
        env['SERVER_NAME']       = WSGIServer.server_name       # localhost
        env['SERVER_PORT']       = str(WSGIServer.server_port)  # 8888
        return env

    def start_response(status, response_headers, exc_info=None):
        # Add necessary server headers
        server_headers = [
            ('Date', 'Mon, 15 Jul 2019 5:54:48 GMT'),
            ('Server', 'WSGIServer 0.2'),
        ]
        WSGIServer.headers_set = [status, response_headers + server_headers]
        # To adhere to WSGI specification the start_response must return
        # a 'write' callable. We simplicity's sake we'll ignore that detail
        # for now.
        # return WSGIServer.finish_response

    def finish_response(result):
        try:
            status, response_headers = WSGIServer.headers_set
            response = f'HTTP/1.1 {status}\r\n'
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data.decode('utf-8')
            # Print formatted response data a la 'curl -v'
            print(''.join(
                f'> {line}\n' for line in response.splitlines()
            ))
            response_bytes = response.encode()
            WSGIServer.client_connection.sendall(response_bytes)
        finally:
            WSGIServer.client_connection.close()


SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 1024


def grim_reaper(signum, frame):
    while True:
        try:
            pid, status = os.waitpid(
                -1,          # Wait for any child process
                 os.WNOHANG  # Do not block and return EWOULDBLOCK error
            )
        except OSError:
            return

        if pid == 0:  # no more zombies
            return

def handle_one_request(client_connection):
    request_data = client_connection.recv(1024)
    request_data = request_data.decode('utf-8')
    # Print formatted request data a la 'curl -v'
    print(''.join(
        f'< {line}\n' for line in request_data.splitlines()
    ))

    WSGIServer.parse_request(request_data)

    # Construct environment dictionary using request data
    env = WSGIServer.get_environ()

    # It's time to call our application callable and get
    # back a result that will become HTTP response body
    result = WSGIServer.application(env, WSGIServer.start_response)

    # Construct a response and send it back to the client
    WSGIServer.finish_response(result)

def make_server(server_address, application):
    server = WSGIServer(server_address)
    server.set_app(application)
    return server

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print(f"""
|___  /
   / /   ___  _ __   _ __    ___  _ __
  / /   / _ \| '_ \ | '_ \  / _ \| '__|
./ /___|  __/| |_) || |_) ||  __/| |
\_____/ \___|| .__/ | .__/  \___||_|
             | |    | |
             |_|    |_|
""")
    print(f'Welcome to Zepper \n')
    print(f'WSGIServer: Serving HTTP on port {PORT} ...\n')
    httpd.serve_forever()
