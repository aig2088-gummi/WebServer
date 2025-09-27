# import socket module
from socket import *
# In order to terminate the program
import sys


def webServer(port=13331):
    # Create a TCP socket using IPv4
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Allow the port to be reused right after program exit
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)f

    # Prepare a server socket
    serverSocket.bind(("", port))

    # Start listening for incoming connections (max 1 queued connection here)
    serverSocket.listen(1)
    print("Server is ready to serve on port...", port)

    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()  # Accept a client connection

        try:
            # Receive client request
            message = connectionSocket.recv(1024).decode()
            print("Request:", message)

            # Get the requested filename from the HTTP request line
            filename = message.split()[1]

            # Open the requested file
            f = open(filename[1:], "rb")  # Open in binary mode since we’ll send over socket

            # Create HTTP response header for 200 OK
            header = "HTTP/1.1 200 OK\r\n"
            header += "Content-Type: text/html; charset=UTF-8\r\n"
            header += "\r\n"  # Blank line to end headers

            # Read file content
            file_content = f.read()

            # Send header + file content
            connectionSocket.sendall(header.encode() + file_content)

            # Close the connection
            connectionSocket.close()

        except Exception as e:
            # Send 404 response if file not found or another error occurs
            header = "HTTP/1.1 404 Not Found\r\n"
            header += "Content-Type: text/html; charset=UTF-8\r\n"
            header += "\r\n"
            body = "<html><body><h1>404 Not Found</h1></body></html>"

            # Send header + error message
            connectionSocket.sendall(header.encode() + body.encode())

            # Close the connection
            connectionSocket.close()

    # Never reached in Gradescope, left here for local testing
    # serverSocket.close()
    # sys.exit()  # Terminate the program after sending the corresponding data


if __name__ == "__main__":
    webServer(13331)
