import json
import time
import base64
from socket import *

discovered_users = {}

serverIP = '127.0.0.1'
serverPort = 6001
def secure_chat():
  clientsocket = socket(AF_INET, SOCK_STREAM)
  clientsocket.connect((serverIP, serverPort))
  publickey = input('Input key: ')
  dictionary = {
    "key": publickey
  }
  json_object = json.dumps(dictionary, indent=3)
  clientsocket.send(json_object.encode())
  data = clientsocket.recv(1024).decode()
  received_key = json.loads(data)
  key=((2^int(publickey)%19)^int(received_key['key']))%19
  print("Enter your message: ")
  message = input()
  encrypted_message = {
    "encrypted_message": base64.b64encode(message.encode()).decode()
  }
  json_message = json.dumps(encrypted_message,indent=1)
  clientsocket.send(json_message.encode())
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

secure_chat()

mode = input("Please enter Users, History or Chat")
if mode == "Users":
  display_users()
elif mode == "History":
  pass
elif mode == "Chat":
  chatuser=input("Please enter Username")

  with open('discovered.json','r') as outfile:
    data = json.load(outfile)
    for username in data:
      for info in data[username]:
        if info == 'username'
          print(f"{username} " + "Online")
        elif info == 'username'
          print(f"{username} " + "Away")