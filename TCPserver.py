from socket import *
import json
import base64

serverPort = 6001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen()   # TCP server is listening for connections
print('The server is ready to receive')

my_public_key = 5


while True:  # welcoming socket continues listening even after user leaves
    connectionSocket, addr = serverSocket.accept()
    print(f"Connection established with {addr}")

    while True:  # be ready to receive and capitalize more than 1 msg
        message = connectionSocket.recv(1024)

        thing = json.loads(message)
        print(thing)


        if "key" in thing:
            print("Key received from client. Generating and sending my public key...")
            received_key = int(thing['KEY'])
            key = ((2 ^ int(my_public_key) % 19) ^ received_key) % 19

            response = {
                "key": str(my_public_key)
            }
            response_json = json.dumps(response)
            connectionSocket.send(response_json.encode())
            print(f"My public key sent: {my_public_key}")

        else:


    connectionSocket.close()

serverSocket.close()
