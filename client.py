import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 1234

# Input password
password = input("Enter the server password: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = None  # To store the username globally

# Listening to server messages
def receive_messages():
    global username
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "PASSWORD":
                client.send(password.encode('utf-8'))
            elif message == "USER":
                username = input("Enter your username: ")
                client.send(username.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

# Sending messages to the server
def send_messages():
    while True:
        message = input()
        client.send(f'{message}'.encode('utf-8'))

# Starting threads for listening and sending
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
