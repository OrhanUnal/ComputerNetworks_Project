import json
import time
from socket import *
serverPort = 6000
serverSocket = socket( AF_INET , SOCK_DGRAM )
serverSocket.bind(( '', serverPort ))
print ('The server is ready to receive')

discovered_users = {}

while True:
   message, clientAddress = serverSocket.recvfrom(1024)
   message = message.decode('utf-8')
   try:
      message_json = json.loads(message)
      if 'username' in message_json:
         username = message_json['username'].lower()
         discovered_users[username] = {"ip": clientAddress[0], "timestamp": time.time()}
         print(f"Detected user: {username} is online")
         with open('discovered.json', 'w') as outfile:
            json.dump(discovered_users, outfile)
            outfile.write("\n")
   except json.JSONDecodeError:
      print("Error: Invalid JSON format")
serverSocket.close()




