import socket
import sys

serverIP = "127.0.0.1"  # The server's hostname or IP address
serverPORT = 65432  # The port used by the server

filename = sys.argv[1]

# Open the file in read mode
with open(filename, "r") as file:
    for line in file:

        line = line.strip()
        # process line
        print("Input request: " + line)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
            clientSocket.connect((serverIP, serverPORT))
            clientSocket.sendall(line.encode())
            [status_code, result] = clientSocket.recv(1024).decode().split()

            if status_code == "200":
                print("The result is: " + result)
            elif status_code == "620":
                print(f"Error {status_code}: Invalid Operation Code (i.e, not +, -, *, or /)")
            else:
                print(f"Error {status_code}: Either non-integer operands, or division by 0")
