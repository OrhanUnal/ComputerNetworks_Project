import json
from socket import *
from time import sleep

serverIP = '192.168.1.255'  # broadcast
serverPort = 6000

clientSocket = socket(AF_INET, SOCK_DGRAM)
sentence = input('Input lowercase username: ')
dictionary = {
  "username":  sentence
}


while 1:
  json_object = json.dumps(dictionary, indent = 3)
  clientSocket.sendto(json_object.encode(), (serverIP, serverPort))
  modifiedSentence, serverAddress = clientSocket.recvfrom(1024)
  print ('From Server:', modifiedSentence.decode())
  sleep(8)
clientSocket.close()
