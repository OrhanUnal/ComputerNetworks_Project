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
  sleep(8)
clientSocket.close()
