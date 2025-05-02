import json
import time
import base64
from contextlib import nullcontext
from datetime import datetime
from pyDes import des, CBC, PAD_PKCS5
from socket import *

log = {}

connected = False

serverIP = '192.168.127.12'
serverPort = 6001

clientsocket = socket(AF_INET, SOCK_STREAM)

def secure_chat(user_name):
  publickey = input('Input key: ')
  publickey = int(publickey) % 19
  dictionary = {
    "key": publickey
  }
  json_object = json.dumps(dictionary, indent=3)
  clientsocket.send(json_object.encode())
  data = clientsocket.recv(1024).decode()
  received_key = json.loads(data)
  key = str(((2^int(publickey)%19)^int(received_key['key']))%19)
  key = base64.urlsafe_b64encode(key.encode()).ljust(8, b'0')
  pydes = des(key, CBC, key, pad=None, padmode=PAD_PKCS5)
  message = input("Enter your message: ")
  write_to_log(message, user_name)
  encrypted = base64.b64encode(pydes.encrypt(message)).decode()
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
  try:
    with open("chat_log.json", "r") as input_file:
      if input_file != nullcontext:
        data = json.load(input_file)
        for line in data:
          log[line] = {"username": data[line]['username'], "message": data[line]['message'], "sent": data[line]['sent']}
  except FileNotFoundError:
    print("Creating your chat log file ")
  log[datetime.now().strftime("%H:%M:%S")] = {"username": user_name, "message": message, "sent": "SENT"}
  with open('chat_log.json', 'w') as output_file:
    json.dump(log, output_file)
    output_file.write("\n")

def history(name):
  history_found = False
  try:
    with open('chat_log.json', 'r') as outfile:
      if outfile != nullcontext:
        log = json.load(outfile)
        for data in log:
          if log[data]['username'] == name:
            history_found = True
            print("At " + data + " " + str(log[data]['username']) + " " + log[data]['sent'] + "   " + log[data]['message'] + " ")
  except FileNotFoundError:
    print("There is no history file ")
  if not history_found:
    print("There is no history for " + name)

user_found = False
while True:
  mode = input("Please enter Users, History or Chat: ").lower()
  if mode == "users" or mode == "user":
    display_users()
  elif mode == "history":
    history_name = input("Please enter that person's name: ")
    history(history_name)
  elif mode == "chat":
    chat_user = input("Please enter Username: ").lower()
    with open('discovered.json','r') as outfile:
      data = json.load(outfile)
      for username in data:
        if username == chat_user and time.time() - data[username]['timestamp'] < 900:
          user_found = True
          serverIP = data[username]['ip']
          if not connected:
            try:
              clientsocket.connect((serverIP, serverPort))
              connected = True
            except:
              print("Connection failed")
          security = input("Do you want to chat securely or not?\n" + "Please enter Secure or Unsecure: ").lower()
          if security == "secure":
            secure_chat(username)
          elif security == "unsecure":
            unsecure_chat(username)
          else:
            print("Please enter Secure or Unsecure: ")
          break
      if not user_found:
        print("That username is not registered or the person you are trying to reach is not available")