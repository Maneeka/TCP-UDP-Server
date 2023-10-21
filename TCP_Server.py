import socket

serverPort = 65432

# Helper function to compute the result
def compute_result(operator, operand1, operand2):
    if operator == '+':
        return operand1 + operand2
    elif operator == '-':
        return operand1 - operand2
    elif operator == '*':
        return operand1 * operand2
    elif operator == '/':
        return operand1 / operand2


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", serverPort))
    s.listen(1)
    print('the server is ready to receive')

    connectionSocket, addr = s.accept()

    with connectionSocket:
        print(f"Connected by {addr}")
        while True:
            request = connectionSocket.recv(1024).decode().split()

            if not request:    # connection with client has ended
                break

            [oc, op1, op2] = request
            response = ''
            status_code = result = -1

            # check validity of request
            if oc not in ('+', '-', '*', '/'):
                status_code = 620  # send error code 620 with -1 result
                result = -1

            else:

                # Check if the received request contains valid integers
                try:
                    received_op1 = int(op1)
                    received_op2 = int(op2)

                    if oc == '/' and received_op2 == 0:  # division by 0
                        status_code = 630
                        result = -1
                    else:
                        status_code = 200  # Successful integers received
                        result = compute_result(oc, received_op1, received_op2)

                except ValueError:  # Non-integer data received
                    status_code = 630
                    result = -1

                response = str(status_code) + " " + str(result)
                print(' '.join(request) + ' -> ' + response)
                connectionSocket.sendall(response.encode())
