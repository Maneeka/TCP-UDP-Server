import socket

serverIP = "127.0.0.1"  # The server's hostname or IP address
serverPORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    clientSocket.connect((serverIP, serverPORT))
    clientSocket.sendall(b"+ 100 -1")
    data = clientSocket.recv(1024)

print(f"Received {data!r}")