# Import socket programming library
import socket

# Import thread module
from _thread import *
import threading
import logging
import hashlib
import time
from threading import Thread


# Thread function
# Socket is the socket object with which connection was made, used to send and receive messages
def threaded(socket, threadNum):

    m = hashlib.sha256()
    logging.info("SERVER thread #%s: iniciando", threadNum)
    print("SERVER thread #", threadNum,
          ". El archivo que se va a abrir es: ", file)
    logging.info("SERVER thread #%s: el archivo abierto fue %s ",
                 threadNum, file)
    with open(file, 'rb') as f:

        # Data received from client
        data = f.read()

        m.update(data)
        start_time = time.time()
        # Send back reversed string to client
        numBytes = socket.send(data)

        print("Fin de envío thread #", threadNum)

        # Send hash
        h = m.hexdigest()
        print("Digest enviado: ", h)
        numBytesHash = socket.send(("HASHH" + h).encode())

        logging.info('SERVER thread #%s: bytes enviados sin hash %s',
                     threadNum, numBytes)

        logging.info('SERVER thread #%s: bytes enviados en total %s',
                     threadNum, numBytes + numBytesHash)

    logging.info('SERVER thread #%s: tiempo del envío %s', threadNum,
                 (time.time()-start_time))

 # Connection closed
    socket.close()


def main():
    logging.basicConfig(filename="./serverFiles/serverLog.log", level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S'
                        )

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

        t = Thread(target=threaded, args=(clientsocket, len(threads)))
        threads.append(t)

        # In case you want to start the threads at once
        #start_new_thread(threaded, (clientsocket,))

        if len(threads) == num_conn:
            for i in threads:
                i.start()
            threads = []
            logging.info('SERVER: reiniciando threads')
    serversocket.close()


main()
