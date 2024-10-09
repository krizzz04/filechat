import socket
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 1234

# Passwords
REAL_PASSWORD = "wick"
FAKE_PASSWORD = "admin"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

real_clients = []
fake_clients = []
usernames = []
fake_usernames = ["FakeUser1", "FakeUser2", "FakeBot"]  # Fake usernames for the fake environment

# Broadcast function to real clients
def broadcast(message, client_type="real"):
    if client_type == "real":
        for client in real_clients:
            client.send(message)
    elif client_type == "fake":
        for client in fake_clients:
            client.send(message)

# Handle real client communication
def handle_real_client(client, username):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            broadcast(f'{username}: {message}'.encode('utf-8'), "real")
        except:
            index = real_clients.index(client)
            real_clients.remove(client)
            client.close()
            broadcast(f'{username} left the real chat.'.encode('utf-8'), "real")
            usernames.remove(username)
            break

# Handle fake client communication
def handle_fake_client(client, username):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            fake_broadcast_msg = f'{username}: {message}'  # Show user's message
            broadcast(fake_broadcast_msg.encode('utf-8'), "fake")
            
            # Simulate some responses from fake users
            for fake_user in fake_usernames:
                fake_response = f'{fake_user}: Hello! Welcome to the fake chat!'
                broadcast(fake_response.encode('utf-8'), "fake")
        except:
            index = fake_clients.index(client)
            fake_clients.remove(client)
            client.close()
            break

# Main function to receive connections
def receive_connections():
    print("Server is running and listening...")
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        # Ask for a password
        client.send("PASSWORD".encode('utf-8'))
        password = client.recv(1024).decode('utf-8')
        
        if password == REAL_PASSWORD:
            # Handle real users
            client.send("USER".encode('utf-8'))
            username = client.recv(1024).decode('utf-8')
            usernames.append(username)
            real_clients.append(client)
            
            print(f"Real User: {username}")
            broadcast(f"{username} joined the real chat.".encode('utf-8'), "real")
            client.send("Connected to the REAL server.".encode('utf-8'))
            
            thread = threading.Thread(target=handle_real_client, args=(client, username))
            thread.start()

        elif password == FAKE_PASSWORD:
            # Handle fake users
            client.send("USER".encode('utf-8'))
            username = client.recv(1024).decode('utf-8')
            fake_clients.append(client)
            
            print(f"Fake User: {username}")
            client.send("Connected to the FAKE server.".encode('utf-8'))
            
            thread = threading.Thread(target=handle_fake_client, args=(client, username))
            thread.start()
        
        else:
            client.send("Incorrect password. Connection closed.".encode('utf-8'))
            client.close()

receive_connections()
