# import socket module
from socket import *
# In order to terminate the program
import sys


def webServer(port=13331):
    # Create a TCP socket using IPv4
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Allow immediate reuse of the port after the server stops
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    # Prepare a server socket: bind it to the given port and start listening
    serverSocket.bind(("", port))
    serverSocket.listen(1)  # Queue up to 1 client connection
    print("Ready to serve on port...", port)

    while True:
        print('Waiting for connection...')
        # Accept client connection
        connectionSocket, addr = serverSocket.accept()
        print(f"Connection established with {addr}")

        try:
            # Receive client request
            message = connectionSocket.recv(1024).decode()
            print("Request received:\n", message)

            # Parse filename from HTTP GET request (second token after 'GET')
            filename = message.split()[1]

            # Open the requested file (strip leading slash, open in binary mode)
            f = open(filename[1:], 'rb')

            # Build a valid HTTP response header
            header = "HTTP/1.1 200 OK\r\n"
            header += "Content-Type: text/html; charset=UTF-8\r\n"
            header += "Server: SimplePythonServer\r\n"
            header += "Connection: close\r\n"
            header += "\r\n"  # Blank line signals end of header

            # Read the file content
            fileContent = f.read()

            # Send header and file content together
            connectionSocket.sendall(header.encode() + fileContent)

            # Close file and client connection
            f.close()
            connectionSocket.close()

        except Exception:
            # File not found or another error occurred -> send 404 response
            header = "HTTP/1.1 404 Not Found\r\n"
            header += "Content-Type: text/html; charset=UTF-8\r\n"
            header += "Server: SimplePythonServer\r\n"
            header += "Connection: close\r\n"
            header += "\r\n"

            # Simple HTML body for error message
            body = "<html><head></head><body><h1>404 Not Found</h1></body></html>"

            # Send the error response
            connectionSocket.sendall(header.encode() + body.encode())

            # Close the client connection
            connectionSocket.close()


# Entry point
if __name__ == "__main__":
    webServer(13331)
