import json
import time
import base64
import pyDes
from socket import *

discovered_users = {}

serverIP = '192.168.127.12'
serverPort = 6001

clientsocket = socket(AF_INET, SOCK_STREAM)

def secure_chat():
  publickey = input('Input key: ')
  dictionary = {
    "key": publickey
  }
  json_object = json.dumps(dictionary, indent=3)
  clientsocket.send(json_object.encode())
  data = clientsocket.recv(1024).decode()
  received_key = json.loads(data)
  key=((2^int(publickey)%19)^int(received_key['KEY']))%19
  bytekey = key.to_bytes(8,'big')
  print("Enter your message: ")
  message = input()
  k = pyDes.des(bytekey, pyDes.ECB, padmode=pyDes.PAD_PKCS5)
  encrypted = k.encrypt(message)
  print("encyripted data: " , encrypted)

  encrypted_message = {
    "encrypted_message": base64.b64encode(encrypted)
  }
  json_message = json.dumps(str(encrypted_message),indent=1)
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



while True:
  mode = input("Please enter Users, History or Chat: ").lower()
  if mode == "users" or mode == "user":
    display_users()
  elif mode == "history":
    pass
  elif mode == "chat":
    chat_user = input("Please enter Username: ")
    with open('discovered.json','r') as outfile:
      data = json.load(outfile)
      for username in data:
        if username == chat_user and time.time() - data[username]['timestamp'] < 900:
          serverIP = data[username]['ip']
          clientsocket.connect((serverIP, serverPort))
          security = input("Do you want to chat securely or not?\n" + "Please enter Secure or Unsecure: ").lower()
          if security == "secure":
            secure_chat()
          else:
            #unsecure_chat()
            pass
          clientsocket.close()
        else:
          print("That username is not registered or the person you are trying to reach is not available")