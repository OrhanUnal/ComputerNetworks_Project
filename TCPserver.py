from socket import *
import json
from cryptography.fernet import Fernet
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
            response = {
                "key": my_public_key
            }
            response_json = json.dumps(response)
            connectionSocket.send(response_json.encode())
            print("Key received from client. Generating and sending my public key...")
            received_key = int(thing['key'])
            key = str(((2 ^ int(my_public_key) % 19) ^ received_key) % 19)
            key = base64.urlsafe_b64encode(key.encode().ljust(32, b'0'))
            print(key)
            fernet = Fernet(key)
            print(f"My public key sent: {my_public_key}")

        elif "encrypted_message" in thing:

           received_message = thing['encrypted_message'].encode()
           print(received_message)
           received_message = fernet.decrypt(received_message)
           print("Decrypted message: ", received_message.decode())

        elif "unencrypted_message" in thing:
            received_message = thing['unencrypted_message'].encode()
            print(received_message)
            received_message = base64.b64decode(received_message)
            print("Decrypted message: ",received_message.decode())




    connectionSocket.close()

serverSocket.close()