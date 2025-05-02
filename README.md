# ComputerNetworks_Project

P2P Chat Project

Features

Real-time messaging between clients.
Basic command-line interface.
Support for multiple clients connecting to the server simultaneously.
Real time status of users (online/away).
Private chat option between users
Encrypted message in private sessions.
Private chat option between users
Encrypted message in private sessions.

Installation

Clone the repository: git clone https://github.com/yourusername/NetworkProject.git
Navigate to the project directory: cd chat-project
Install dependencies: pip install $ pip install pydes

Usage

    Broadcast
    Run the broadcaster tool: python Announcement.py
    The client will prompt you to enter your username.
    Once the user enters a name, it will start to announce that the user is online and able to connect.

    Discover
    Run the discover tool: python PeerDiscover.py
    The server will lisen to port 6000 and if any other user announcing their presence, this tool will take that users ip address and name.


    Server
    Run the server: python ChatResponder.py
    The server will start listening for connections on port 6001.
    Once the server is running, clients can connect to it.

    Client
    Run the client: python ChatInitator.py
    The client will prompt you to enter a command.
    User can chat with avaible users, see the name of the avaible users and see the chat history with other users.

        Chat
        ChatInitator will prompt you to enter a username.
        If that user is avaible ChatInitator will try to establish a connection.
        Once connected you can choose whether secure communication or unsecure communication.
        User needs to enter "secure" or "unsecure".

            Secure Chat
            ChatInitator will ask you to enter a integer to send a public key and will send that key to the end user.
            ChatInitator needs to recieve another key from the person that user is talking.
            After getting two different key, ChatInitator will create a common key with Diffie-Hellman key exchange method.
            While ChatInitator creating common key, it will also ask to enter the message that user wants to send.
            After that ChatInitator will encrypt the message and send a JSON object to end user.

            Unsecure Chat
            ChatInitator will ask to enter the message that user wants to send.
            After that it will send a JSON object to end user.

        History
        ChatInitator will prompt you to enter a username.
        After that ChatInitator will write every message between user and the end user.

        Users 
        ChatInitator will list all of the users that is avaible.
        If a user did not broadcast their presence for 10 second, ChatInitator will categorize them as "Away".
        If a user did not broadcast their presence for 15 minutes, ChatInitator will delete their name from avaible users list.