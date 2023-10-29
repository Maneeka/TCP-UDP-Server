import socket

serverIP = "127.0.0.1"
serverPort = 65432

filename = input("Enter input file name: ")

# Open the file in read mode
with open(filename, "r") as file:
    for line in file:

        line = line.strip()
        # process line
        print("Input request: " + line)

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as clientSocket:
            clientSocket.sendto(line.encode(), (serverIP, serverPort))
            response, serverAddr = clientSocket.recvfrom(1024)

            [status_code, result] = response.decode().split()

            if status_code == "200":
                print("The result is: " + result)
            elif status_code == "620":
                print(f"Error {status_code}: Invalid Operation Code (i.e, not +, -, *, or /)")
            else:
                print(f"Error {status_code}: Either non-integer operands, or division by 0")
