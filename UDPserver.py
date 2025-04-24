import time
from socket import *
serverPort = 6000
serverSocket = socket( AF_INET , SOCK_DGRAM )
serverSocket.bind(( '', serverPort ))
print ('The server is ready to receive')

while True:
   message, clientAddress = serverSocket.recvfrom(1024)
   message = message.decode() + str(clientAddress)
   with open("username.json", 'a') as outfile:
      outfile.write(message + '\n')
   capitalizedMessage = message.upper()
   serverSocket.sendto(capitalizedMessage.encode(), clientAddress)
      
serverSocket.close()




