from socket import *  # Import all socket functions


def webServer(port=13331):
    # Create a TCP socket (like a door for communication)
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Bind the socket to the local host and the given port
    serverSocket.bind(("", port))

    # Start listening for incoming connections (1 at a time)
    serverSocket.listen(1)
    print("Server is running on port", port)

    while True:
        # Wait for a client (web browser) to connect
        connectionSocket, addr = serverSocket.accept()

        try:
            # Read the HTTP request message from the client
            message = connectionSocket.recv(1024).decode()

            # Extract the requested filename from the message
            filename = message.split()[1]  # e.g., "/index.html"

            # Open the requested file (skip the first "/" in the filename)
            f = open(filename[1:], 'r')
            outputdata = f.read()
            f.close()  # Close the file after reading

            # --- Send HTTP 200 OK headers ---
            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())  # Status line
            connectionSocket.send("Server: SimpleServer\r\n".encode())  # Server header
            connectionSocket.send("Connection: close\r\n".encode())  # Close after response
            connectionSocket.send("Content-Type: text/html\r\n".encode())  # File type
            connectionSocket.send("\r\n".encode())  # Blank line signals end of headers

            # Send the content of the requested file
            connectionSocket.send(outputdata.encode())

        except:
            # --- File not found: send HTTP 404 headers ---
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())  # Status line
            connectionSocket.send("Server: SimpleServer\r\n".encode())  # Server header
            connectionSocket.send("Connection: close\r\n".encode())  # Close after response
            connectionSocket.send("Content-Type: text/html\r\n".encode())  # File type
            connectionSocket.send("\r\n".encode())  # End of headers

            # Send a simple HTML 404 page
            connectionSocket.send("<h1>404 Not Found</h1>".encode())

        # Close the connection to the client
        connectionSocket.close()


# Run the server if this file is executed
if __name__ == "__main__":
    webServer(13331)