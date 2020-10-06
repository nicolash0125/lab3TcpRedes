# Import socket programming library
import socket

# Import thread module
from _thread import *
import threading
import logging
import hashlib
import time
from threading import Thread
# print_lock = threading.Lock()
logging.basicConfig(filename="./serverFiles/serverLog.log", level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )


# Thread function
# Socket is the socket object with which connection was made, used to send and receive messages
def threaded(socket):

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
        h = m.hexdigest()
        print("Digest enviado: ", h)
        socket.send(("HASHH" + h).encode())

 # Connection closed
    socket.close()


def main():

    global file

    # Initializes the server log
    host = socket.gethostname()
    # Port number
    port = 50000
    logging.info('Connected to %s on port %s', host, port)

    # Socket del servidor
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host, port))
    print('Port: ', port)

    # Become a server socket
    serversocket.listen(5)
    print("Socket listening")
    inputText = int(input("\n ¿Qué archivo desea enviar?"
                          "\n 1. 145 MB"
                          "\n 2. 355 MB"
                          "\n 3. 200 MB \n"))
    if inputText == 1:
        f = "./data/Redes5G.mp4"
    elif inputText == 2:
        f = "./data/Vivaldi.mp4"
    else:
        f = "./data/200MB.zip"

    file = f
    print("Archivo seleccionado: ", file)
    global num_conn
    num_conn = int(
        input('\n ¿A partir de cuántas conexiones desea enviar? \n'))
    logging.info('SERVER: el número de conexiones definido es %s', num_conn)
    print("Esperando conexiones...")

    # Threads connect
    threads = []
    while True:
        # Accept connections from outside
        (clientsocket, address) = serversocket.accept()
        # lock acquired by client
        # print_lock.acquire()
        print('Connected to : ', address[0], ':', address[1])

        t = Thread(target=threaded, args=(clientsocket,))
        threads.append(t)

        # In case you want to start the threads at once
        #start_new_thread(threaded, (clientsocket,))

        if len(threads) == num_conn:
            for i in threads:
                i.start()
            threads = []
    serversocket.close()


main()
