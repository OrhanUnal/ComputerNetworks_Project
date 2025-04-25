import json
from asyncio import wait_for
from socket import *
from time import sleep

serverIP = '127.0.0.255'  # localhost
serverPort = 6000

clientSocket = socket(AF_INET, SOCK_DGRAM)


while 1:
  sentence = input('Input lowercase username: ')
  dictionary = {
    "username":  sentence
  }
  json_object = json.dumps(dictionary, indent = 3)
  clientSocket.sendto(json_object.encode(), (serverIP, serverPort))
  modifiedSentence, serverAddress = clientSocket.recvfrom(1024)
  print ('From Server:', modifiedSentence.decode())
  sleep(8)
clientSocket.close()
