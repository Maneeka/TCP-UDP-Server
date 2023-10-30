import socket
import sys

serverIP = "127.0.0.1"
serverPort = 65432

filename = sys.argv[1]

with open(filename, "r") as file:
    for line in file:
        line = line.strip()
        # process line
        print("Input request: " + line)

        # initialize timer value and other vars
        d = 0.1
        status_code = response = result = None

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as clientSocket:
            while d <= 2:
                try:
                    clientSocket.sendto(line.encode(), (serverIP, serverPort))

                    # start timer
                    clientSocket.settimeout(d)

                    response, serverAddr = clientSocket.recvfrom(1024)
                    [status_code, result] = response.decode().split()   # A reply is received before a timeout.

                    if response is not None:    # response received
                        break

                except socket.timeout:
                    d *= 2
                    if d > 2:
                        status_code = "300"
                        print('Request timed out: the server is DEAD')
                        break
                    else:
                        print('Request timed out: resending')
                        continue    # go back to re-sending the line to the server


            if status_code == "200":
                print("The result is: " + result)
            elif status_code == "620":
                print(f"Error {status_code}: Invalid Operation Code (i.e, not +, -, *, or /)")
            elif status_code == "630":
                print(f"Error {status_code}: Either non-integer operands, or division by 0")
            else:
                print(f"Error {status_code}: server was dead")
