from socket import *
import json
from cryptography.fernet import Fernet
import base64
from datetime import datetime

serverPort = 6001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen()   # TCP server is listening for connections
print('The server is ready to receive')

log = {}

my_public_key = 5

def write_to_log(message, user_name):
    with open("chat_log.json", "r") as input_file:
        data = json.load(input_file)
        for line in data:
            log[line] = {"username": data[line]['username'], "message": data[line]['message'], "sent": data[line]['sent']}
    log[datetime.now().strftime("%H:%M:%S")] = {"username": user_name, "message": message, "sent": "RECEIVED"}
    with open('chat_log.json', 'w') as output_file:
        json.dump(log, output_file)
        output_file.write("\n")

while True:  # welcoming socket continues listening even after user leaves
    connectionSocket, addr = serverSocket.accept()
    print(f"Connection established with {addr}")
    name = "UNDEFINED"
    with open("discovered.json", "r") as file:
        data = json.load(file)
        for line in data:
            if data[line]['ip'] == addr[0]:
                name = line['username']
    while True:  # be ready to receive and capitalize more than 1 msg
        message = connectionSocket.recv(1024)
        thing = json.loads(message)

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
            fernet = Fernet(key)
        elif "encrypted_message" in thing:
           received_message = thing['encrypted_message'].encode()
           print(received_message)
           received_message = fernet.decrypt(received_message)
           print("Secure message: ", received_message.decode())
           write_to_log(received_message.decode(), name)
        elif "unencrypted_message" in thing:
            received_message = thing['unencrypted_message'].encode()
            print(received_message)
            received_message = base64.b64decode(received_message)
            print("Unsecure message: ",received_message.decode())
            write_to_log(received_message.decode(), name)



    connectionSocket.close()

serverSocket.close()