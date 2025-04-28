from socket import *
import json
from urllib.parse import to_bytes

import pyDes
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
            received_key = int(thing['key'])
            print(received_key)
            key = ((2 ^ int(my_public_key) % 19) ^ received_key) % 19

            response = {
                "key": str(my_public_key)
            }
            response_json = json.dumps(response)
            connectionSocket.send(response_json.encode())

            print(f"My public key sent: {my_public_key}")

        elif "encrypted_message" in thing:

           received_message = thing['encrypted_message']
           received_message = received_message.d
           k = pyDes.des(key, pyDes.ECB, padmode=pyDes.PAD_PKCS5)
           decrypted = k.decrypt(received_message)
           print("Decrypted message:", decrypted.decode())




    connectionSocket.close()

serverSocket.close()
0