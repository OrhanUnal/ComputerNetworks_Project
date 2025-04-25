import json
import time
from socket import *

discovered_users = {}

serverIP = '127.0.0.1'
serverPort = 6001

currentTime = time.time()
with open('discovered.json','r') as outfile:
  data = json.load(outfile)
  for username in data:
    for info in data[username]:
      print(data[username][info])

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverIP,serverPort))
while True:
  sentence = input('Input lowercase sentence:')
  clientSocket.send(sentence.encode())
  modifiedSentence = clientSocket.recv(1024).decode()
  print (f"From Server: {modifiedSentence}")
clientSocket.close()