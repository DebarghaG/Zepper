"""
This is a very simple demo that can be used to demonstrate how http requests
and a web server work
"""
import socket

HOST, PORT = '', 8888

"""
This is therefore a networking server, that sits on a physical server and waits for a client to send a request. When it receives a request, it generates a response and sends it back to the client.
The communication between a client and a server happens using HTTP protocol.
A client can be your browser or any other software that speaks HTTP.
"""
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
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
print(f'Serving HTTP on port {PORT} ...')
while True:
    client_connection, client_address = listen_socket.accept()
    request_data = client_connection.recv(1024)
    print(request_data.decode('utf-8'))

    http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(http_response)
    client_connection.close()


"""
To test this, type out the following in your terminal

~~~~~~~~~~~~~~~
debargha@Dabba-Computer:~$ telnet localhost 8888
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
GET /hello HTTP/1.1
HTTP/1.1 200 OK

Hello, World!
Connection closed by foreign host.
~~~~~~~~~~~~~~~~


For
GET /hello HTTP/1.1
GET : HTTP Method
/hello : The page on the server we want to see
HTTP/1.1 : The HTTP version

For the response :
HTTP/1.1 : HTTP version
200 OK : HTTP Status code and reason
Then the content is sent in the form of Hello world,
This is what your browser displays.

Let's break this : Type abcd in the telnet connection
will still return the same Hello world because
our program just ignores everything and that's what it returns

Now  “How do you run a Django application, Flask application, and Pyramid application under your freshly minted Web server without making a single change to the server to accommodate all those different Web frameworks?”

"""
