from socket import *
import json
serverPort = 6001
serverSocket = socket( AF_INET , SOCK_STREAM )
serverSocket.bind(( '', serverPort ))
serverSocket.listen()   # TCP server is listening  for connections
print ('The server is ready to receive')

while True:  # welcoming socket  continues listening even after user leaves
   connectionSocket, addr = serverSocket.accept()
   print(f"Connection established with {addr}")

   while True:  # be ready to receive and capitalize more than 1 msg
      message = connectionSocket.recv(1024)
      thing = json.loads(message)
      capitalizedMessage = message
      connectionSocket.send(capitalizedMessage)
      print(thing)
   connectionSocket.close()
   
serverSocket.close()