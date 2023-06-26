import socket  # Importa il modulo per la comunicazione tramite socket
import platform  # Importa il modulo per ottenere informazioni sul sistema operativo
import os  # Importa il modulo per interagire con il sistema operativo
import subprocess  # Importa il modulo per eseguire comandi di shell

SRV_ADDR = "192.168.90.101"  # Indirizzo IP del server
SRV_PORT = 8888  # Porta del server

def print_menu():
    print("\n\n1) Ottieni informazioni di sistema\n2) Elenca il contenuto della directory\n3) Avvia la shell\ne) Chiudi la connessione")

my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un oggetto socket
my_sock.connect((SRV_ADDR, SRV_PORT))  # Connette il socket al server
print("Connessione stabilita")
print_menu()

while True:
    message = input("\n-Seleziona un'opzione: ")  # Richiede all'utente di selezionare un'opzione
    if message == "e":
        my_sock.sendall(message.encode())  # Invia il messaggio al server
        my_sock.close()
        break
    elif message == "1":
        my_sock.sendall(message.encode())
        data = my_sock.recv(1024)
        if not data:
            break

        print(bytes(data).decode('utf-8') + bytes("\x1b[0m", encoding='ansi') + bytes("\x1b[0m", encoding='437'))
    elif message == "2":
        path = input("Inserisci il percorso: ")
        my_sock.sendall(message.encode())
        my_sock.sendall(path.encode())
        data = my_sock.recv(1024)
        data = data.decode('utf-8').split(",")
        print("*" * 40)
        for x in data:
            print(x)
        print("*" * 40)
    elif message == "3":
        my_sock.sendall(message.encode())
        data = my_sock.recv(1024).decode('utf-8')
        print(bytes(data, encoding='utf-8') + bytes("\x1b[0m", encoding='ansi') + bytes("\x1b[0m", encoding='437'))
        while True:
            command = input("Inserisci un comando: ")
            my_sock.sendall(command.encode('utf-8'))
            if command.lower() == 'exit':
                break
            output = my_sock.recv(1024).decode('utf-8')
            print(bytes(output, encoding='utf-8') + bytes("\x1b[0m", encoding='ansi') + bytes("\x1b[0m", encoding='437'))
    else:
        print_menu()
