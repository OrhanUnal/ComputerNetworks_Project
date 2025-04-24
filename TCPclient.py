from socket import *
serverIP = '127.0.0.1'
serverPort = 6001
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverIP,serverPort))

while True:
  sentence = input('Input lowercase sentence:')
  clientSocket.send(sentence.encode())
  modifiedSentence = clientSocket.recv(1024).decode()
  print (f"From Server: {modifiedSentence}")
clientSocket.close()