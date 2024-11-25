"""
Detta program implementerar en enkel chattserver som tillåter flera klienter att ansluta och kommunicera med varandra.
Servern använder TCP-sockets för att hantera anslutningar och meddelanden mellan klienterna. 

Funktioner:
- Klienter kan ansluta till servern och ange ett användarnamn.
- Servern sänder meddelanden från en klient till alla andra anslutna klienter.
- Klienter kan lämna chattrummet genom att skicka kommandot "QUIT".

Användning:
1. Starta servern.
2. Klienter kan ansluta till servern via dess IP-adress och portnummer.
3. Klienter kan skicka meddelanden som kommer att broadcastas till alla andra anslutna klienter.
"""


import socket
import threading


HOST = socket.gethostbyname(socket.gethostname()) #Dessa funktioner hämtar den lokala IP-adressen på maskinen programmet körs på.
PORT = 1999 #Portnummer

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Skapar en server socket och tilldelar den till en variabel
server_socket.bind((HOST, PORT)) #Binder server socketen jag skapat till en IP-adress samt en port.
server_socket.listen() #Startar lyssning av servern.
print("Servern lyssnar efter anslutningar...")

client_list: list = [] #Skapar en tom lista där alla klienter som ansluter hamnar.
nickname_list: list = [] #Skapar en tom lista där alla användarnamn som klienterna väljer hamnar.

def accept_clients():
  """
  Denna funktion accepterar alla klienter som ansluter till servern och skapar en tråd för varje klient.
  Denna funktion kommer loopa oändligt.
  """
  while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Ny anslutning från {client_address}")
           
            handle_client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            handle_client_thread.start()

        except Exception as e:
            print(f"Fel vid anslutning av klient {e}")



def handle_client(client_socket, client_address): 
    """
    Denna funktion tar emot användarnamnet som användaren skickar in för att sedan lägga till dem i klient samt nickname listan.
    Två vilkor finns för att kontrollera vad som ska skrivas ut beroende på hur många klienter som är anslutna.
    Sist så skapar vi en tråd som är ansvarig för att ta emot och bearbeta meddelanden från varje klient.
    """
    try:
        nickname = client_socket.recv(1024).decode("UTF-8")
        client_list.append(client_socket)
        nickname_list.append(nickname)
        print(f"Användarnamn för klient: {client_address} är: {nickname}")

        if len(client_list) > 1:
            broadcast_message(f"{nickname} har anslutit till chatten")
        elif len(client_list) == 1:
            message = "Du har anslutit till chatten"
            client_socket.send(message.encode("UTF-8"))

        recive_message_thread = threading.Thread(target=receive_message, args=(client_socket, nickname))
        recive_message_thread.start()
    
    except Exception as e:
            print(f"Fel vid hantering av klient {e}")


def receive_message(client_socket, nickname):
    """
    Denna funktion är till för att ta emot meddelanden från klienterna.
    Jag använder mig av ett try block för att ta emot alla meddelanden och ifall klienten skickar QUIT så skall klienten samt deras användarnamn tas bort från respektive lista.
    Alla andra meddelanden som klienterna skickar kommer broadcastas till alla anslutna klienter.
    Skulle det vara så att klientens anslutning avbryts av något skäl så kommer Exception fånga upp det och "kicka" klienten istället för att servern ska krascha.
    """
    while True:
        try:
            message_from_client = client_socket.recv(1024).decode("UTF-8")
        
            if message_from_client == "QUIT":
                client_list.remove(client_socket)
                nickname_list.remove(nickname)
                client_socket.close()
                print(f"{nickname} har lämnat chattrummet")
                broadcast_message(f"{nickname} har lämnat chattrummet")
                break
            else:
                broadcast_message(f"{nickname}: {message_from_client}")

        except (ConnectionResetError, ConnectionAbortedError):
            client_list.remove(client_socket)
            nickname_list.remove(nickname)
            client_socket.close()
            print(f"{nickname} har lämnat chattrummet")
            broadcast_message(f"{nickname} har lämnat chattrummet")
            break
    

def broadcast_message(message_from_client):
        """
        Denna funktion är till för att skicka ut alla meddelanden som en klient skickar till alla anslutna klienter.
        Även här så använder jag Exception för att fånga upp errors istället för att servern ska krasha. 
        """
        try:
            for clients in client_list:
                clients.send(message_from_client.encode("UTF-8"))
        except Exception:
            print("Fel vid sändning av meddelande")
            
            
accept_clients() #Anropar accept_clients funktionen.