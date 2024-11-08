import socket
import threading


HOST = socket.gethostbyname(socket.gethostname())
PORT = 1999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print("Server is listening for a connection...")

client_list: list = []
nickname_list: list = []


def handle_client():
    while True:
        client_socket, client_address = server_socket.accept()
        client_list.append(client_socket)

        nickname = client_socket.recv(1024).decode("UTF-8")
        nickname_list.append(nickname)
        print(f"Användarnamn för {client_address} heter: {nickname}")

        if len(client_list) > 1:
            broadcast_message(f"{nickname} har anslutit till chatten")
        elif len(client_list) == 1:
            message = "Du har anslutit till chatten"
            client_socket.send(message.encode("UTF-8"))

        recive_message_thread = threading.Thread(target=receive_message, args=(client_socket, nickname, client_address))
        recive_message_thread.start()


def receive_message(client_socket, nickname, client_address):
    while True:
        try:
            message_from_client = client_socket.recv(1024).decode("UTF-8")
        
            if message_from_client == "QUIT":
                client_list.remove(client_socket)
                nickname_list.remove(nickname)
                client_socket.close()
                print(f"{nickname} har lämnat chattrummet")
                broadcast_message(f"{nickname} har lämnat chattrummet")
            else:
                broadcast_message(f"{nickname}: {message_from_client}")

        except Exception as e:
            break
    

def broadcast_message(message_from_client):
        try:
            for clients in client_list:
                clients.send(message_from_client.encode("UTF-8"))
        except Exception as e:
            print("Fel vid sändning av meddelande")
            print(e)
            
        
    

handle_client()






