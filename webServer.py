# import socket module
from socket import *
# In order to terminate the program
import sys




# Example of how to structure the response
response_body = "<h1>Hello, World!</h1>"
content_length = len(response_body.encode('utf-8'))

response_headers = (
    "HTTP/1.1 200 OK\r\n"
    "Server: MyCustomPythonServer\r\n"  # Add the Server header
    "Connection: close\r\n"              # Add the Connection header
    "Content-Type: text/html\r\n"
    f"Content-Length: {content_length}\r\n"
    "\r\n"  # A blank line indicates the end of headers
)

full_response = response_headers.encode('utf-8') + response_body.encode('utf-8')


def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Prepare a server socket
    serverSocket.bind(("", port))
    serverSocket.listen(1)  # Start listening for incoming connections
    print("Ready to serve on port...", port)

    while True:
        # Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()  # Accept client connection

        try:
            message = connectionSocket.recv(1024).decode()  # Receive client message
            filename = message.split()[1]  # Extract the filename from the GET request

            # Open the client requested file (remove the leading slash)
            f = open(filename[1:], 'rb')  # Open file in binary mode

            # Send HTTP response header line for a successful request
            header = "HTTP/1.1 200 OK\r\n"
            Server: PythonWebServer / 1.0
            Connection: close
            contentType = "Content-Type: text/html; charset=UTF-8\r\n"
            endOfHeader = "\r\n"


            # Read the file content
            fileContent = f.read()

            # Send the response header and file content
            response = header + contentType + endOfHeader
            connectionSocket.send(response.encode() + fileContent)

            # Close the file
            f.close()

            # Close the client connection socket
            connectionSocket.close()

        except Exception as e:
            # Send response message for file not found
            header = "HTTP/1.1 404 Not Found\r\n"
            contentType = "Content-Type: text/html; charset=UTF-8\r\n"
            endOfHeader = "\r\n"
            body = "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n"


            response = header + contentType + endOfHeader + body
            connectionSocket.send(response.encode())

            # Close the client connection socket
            connectionSocket.close()


# Entry point
if __name__ == "__main__":
    webServer(13331)