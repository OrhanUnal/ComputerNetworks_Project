import json
import time
from datetime import datetime
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
         username = message_json['username']
         discovered_users[username] = {"ip": clientAddress[0], "timestamp": time.time()}
         print(f"Detected user: {username} ({clientAddress[0]})")
         print(discovered_users[username])
         with open('discovered.json', 'w') as outfile:
            json.dump(discovered_users, outfile)
            outfile.write("\n")
   except json.JSONDecodeError:
      print("Error: Invalid JSON format")

   capitalizedMessage = message.upper()
   serverSocket.sendto(capitalizedMessage.encode(), clientAddress)
      
serverSocket.close()




