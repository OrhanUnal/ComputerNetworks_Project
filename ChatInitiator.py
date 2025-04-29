import json
import time
import base64
from datetime import datetime
from cryptography.fernet import Fernet
from socket import *

log = {}

connected = False

serverIP = '192.168.127.12'
serverPort = 6001

clientsocket = socket(AF_INET, SOCK_STREAM)

def secure_chat(user_name):
  publickey = input('Input key: ')
  dictionary = {
    "key": publickey
  }
  json_object = json.dumps(dictionary, indent=3)
  clientsocket.send(json_object.encode())
  data = clientsocket.recv(1024).decode()
  received_key = json.loads(data)
  key = str(((2^int(publickey)%19)^int(received_key['key']))%19)
  key = base64.urlsafe_b64encode(key.encode().ljust(32, b'0'))
  print(key)
  fernet = Fernet(key)
  message = input("Enter your message: ")
  encrypted = str(fernet.encrypt(message.encode()).decode())
  print(encrypted)
  write_to_log(message, user_name)
  encrypted_message = {
    "encrypted_message": encrypted
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

def unsecure_chat(user_name):
  message = input("Please enter your message: ")
  write_to_log(message, user_name)
  message = base64.b64encode(message.encode()).decode()
  unencrypted_message = {
    "unencrypted_message": message,
  }
  json_message = json.dumps(unencrypted_message, indent=1)
  clientsocket.send(json_message.encode())

def write_to_log(message, user_name):
  log[datetime.now().strftime("%H:%M:%S")] = {"username": user_name, "message": message, "sent": "SENT"}
  print(log)
  with open('chat_log.json', 'w') as outfile:
    json.dump(log, outfile)
    outfile.write("\n")

def history():
  with open('chat_log.json', 'r') as outfile:
    log = json.load(outfile)
    for data in log:
      print(data + " " + str(log[data]['username']) + "      " + log[data]['message'] + " " + log[data]['sent'])

while True:
  mode = input("Please enter Users, History or Chat: ").lower()
  if mode == "users" or mode == "user":
    display_users()
  elif mode == "history":
    history()
  elif mode == "chat":
    chat_user = input("Please enter Username: ")
    with open('discovered.json','r') as outfile:
      data = json.load(outfile)
      for username in data:
        if username == chat_user and time.time() - data[username]['timestamp'] < 900:
          serverIP = data[username]['ip']
          if not connected:
            clientsocket.connect((serverIP, serverPort))
            connected = True
          security = input("Do you want to chat securely or not?\n" + "Please enter Secure or Unsecure: ").lower()
          if security == "secure":
            secure_chat(username)
          elif security == "unsecure":
            unsecure_chat(username)
          else:
            print("Please enter Secure or Unsecure: ")
        else:
          print("That username is not registered or the person you are trying to reach is not available")
          clientsocket.close()