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

def check_valid_operands(oc, op1, op2):  # returns True if operands are valid integers, False otherwise
    try:
        received_op1 = int(op1)
        received_op2 = int(op2)

        if oc == '/' and received_op2 == 0:  # division by 0
            return False
        else:
            return True  # valid integer operands and operations

    except ValueError:  # Non-integer data received
        return False

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as serverSocket:
    serverSocket.bind(("127.0.0.1", serverPort))    # Bind socket to port
    print("UDP server is ready to receive")

    while True:

        [request, clientAddr] = serverSocket.recvfrom(2048)
        request = request.decode().split()

        [oc, op1, op2] = request
        response = ''
        status_code = result = -1

        # check validity of request
        if oc not in ('+', '-', '*', '/'):
            status_code = 620  # send error code 620 with -1 result
            result = -1

        else:

            if check_valid_operands(oc, op1, op2):
                status_code = 200  # Successful integers received
                result = compute_result(oc, int(op1), int(op2))
            else:   # non-valid operands, or division by 0
                status_code = 630
                result = -1

        # send and print response
        response = str(status_code) + " " + str(result)
        print(' '.join(request) + ' -> ' + response)
        serverSocket.sendto(response.encode(), clientAddr)
