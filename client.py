"""
Detta program implementerar en enkel chattklient som ansluter till en chattserver.
Klienten tillåter användaren att välja ett användarnamn och skicka meddelanden till servern.
Meddelanden från servern tas emot och skrivs ut på skärmen.

Funktioner:
- Användaren kan välja ett användarnamn.
- Klienten kan skicka meddelanden till servern.
- Klienten tar emot meddelanden från servern och visar dem i realtid.

Användning:
1. Starta klientprogrammet.
2. Välj ett användarnamn.
3. Skicka meddelanden och ta emot svar från servern.

Notera: Klienten avslutas om användaren skriver "QUIT".
"""

import socket
import threading

HOST = socket.gethostbyname(socket.gethostname()) #Dessa funktioner hämtar den lokala IP-adressen på maskinen programmet körs på.
PORT = 1999 #Portnummer



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Skapar en klient socket och tilldelar den till en variabel.
client_socket.connect((HOST, PORT)) #Ansluter min klient socket till en server med hjälp av HOST och PORT.


def choose_nickname():
    """
    Denna funktion är till för att låta användaren välja ett användarnamn samt skicka det användarnamnet till servern.
    """
    nickname = input("Välj ett användarnamn: ")
    client_socket.send(nickname.encode("UTF-8"))


def receive_message():
    """
    Denna funktion är till för att kunna ta emot meddelanden som skickas från servern och printa det.
    Skulle det vara så att det blir något fel så kommer Exception fånga upp det.
    """
    while True:
        try:
            message = client_socket.recv(1024).decode("UTF-8")
            print(message)

        except Exception as e:
            break

def write_message():
    """
    Denna funktion är till för att kunna skicka meddelanden till servern.
    Villkor för att kontrollera om användaren vill lämna chatten och ifall det stämmer så stängs socketen. Annars så skickas meddelandet till servern.
    """
    while True:
        send_message = input("")
        if send_message == "QUIT":
            client_socket.send(send_message.encode("UTF-8"))
            client_socket.close()
            break

        else:
            client_socket.send(send_message.encode("UTF-8"))
        


choose_nickname() #Anropar choose_nickname funktionen.
receive_message_thread = threading.Thread(target=receive_message) #Skapar en tråd för receive_message funktionen.
write_message_thread = threading.Thread(target=write_message) #Skapar en tråd för write_message funktionen.
receive_message_thread.start() #Startar tråden.
write_message_thread.start() #Startar tråden.

# Vänta på att trådarna ska avslutas
receive_message_thread.join()
write_message_thread.join()