# Import socket programming library
import socket

# Import thread module
from _thread import *
import threading
import logging
import hashlib
import time

# print_lock = threading.Lock()
logging.basicConfig(filename="serverLog.log", level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )


# Thread function
# Socket is the socket object with which connection was made, used to send and receive messages
def threaded(socket):

    while cont < num_conn:
        pass

    start_time = time.time()
    m = hashlib.sha256()
    logging.info("SERVER: iniciando")
    print("El archivo que se va a abrir es: ", file)
    logging.info("SERVER: el archivo abierto fue %s ", file)
    with open(file, 'rb') as f:

        # Data received from client
        data = f.read()

        m.update(data)

        # Send back reversed string to client
        socket.send(data)

        print("Fin de envío")

        # Send hash
        h = str(m.hexdigest())
        print("Digest enviado: ", m.hexdigest())
        socket.send(("HASHH" + h).encode(encoding='ANSI', errors='strict'))

 # Connection closed
    socket.close()


def main():

    global file

    # Initializes the server log
    host = "localhost"
    # Port number
    port = 50000
    logging.info('Connected to %s on port %s', host, port)

    # Socket del servidor
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host, port))
    print('Port %s', port)

    # Become a server socket
    serversocket.listen(5)
    print("Socket listening")
    inputText = int(input("\n ¿Qué archivo desea enviar?"
                          "\n 1. 145 MB"
                          "\n 2. 355 MB"))
    if inputText == 1:
        f = "../videos/Redes5G.mp4"
    else:
        f = "../videos/Vivaldi.mp4"

    file = f
    print("Archivo seleccionado: ", file)
    global num_conn
    num_conn = int(input('\n ¿A partir de cuántas conexiones desea enviar?'))
    logging.info('SERVER: el número de conexiones definido es %s', num_conn)
    print("Esperando conexiones...")

    # Counter with number of connections received
    global cont
    cont = 0
    while True:
        # Accept connections from outside
        (clientsocket, address) = serversocket.accept()
        # lock acquired by client
        # print_lock.acquire()
        print('Connected to : ', address[0], ':', address[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (clientsocket,))
        cont += 1
    serversocket.close()


main()
