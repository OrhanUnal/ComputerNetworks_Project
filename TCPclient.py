import json
import time
from socket import *

discovered_users = {}

serverIP = '127.0.0.1'
serverPort = 6001

def display_users():
  current_time = time.time()
  with open('discovered.json','r') as outfile:
    data = json.load(outfile)
    for username in data:
      for info in data[username]:
        if info == 'timestamp' and current_time - data[username][info] < 10:
          print(f"{username} " + "Online")
        elif info == 'timestamp' and current_time - data[username][info] < 900:
          print(f"{username} " + "Away")

display_users()

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverIP,serverPort))
while True:
  sentence = input('Input lowercase sentence:')
  clientSocket.send(sentence.encode())
  modifiedSentence = clientSocket.recv(1024).decode()
  print (f"From Server: {modifiedSentence}")
clientSocket.close()