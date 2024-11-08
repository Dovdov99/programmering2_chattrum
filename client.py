import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 1999



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def choose_nickname():
    nickname = input("Välj ett användarnamn: ")
    client_socket.send(nickname.encode("UTF-8"))


def recieve_message():
    while True:
        try:
            message = client_socket.recv(1024).decode("UTF-8")
            print(message)

        except Exception as e:
            break

def write_message():
    while True:
        send_message = input("")
        if send_message == "QUIT":
            client_socket.send(send_message.encode("UTF-8"))
            client_socket.close()
            break

        else:
            client_socket.send(send_message.encode("UTF-8"))
        


choose_nickname()
recieve_message_thread = threading.Thread(target=recieve_message)
write_message_thread = threading.Thread(target=write_message)
recieve_message_thread.start()
write_message_thread.start()