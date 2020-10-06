# Import socket module
import socket
import logging
import hashlib
import time
from _thread import *
from threading import Thread
import random


def main():

    cliente_num = random.random()*100000000000
    # Initializes the client log
    logging.basicConfig(filename="./files/client" + str(cliente_num) + ".log", level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S'
                        )
    print('Bienvenido')
    m = hashlib.sha256()
    threaded(m, cliente_num)


def threaded(m, cliente_num):
    start_time = time.time()

    # Local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = 50000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server on local computer
    s.connect((host, port))
    print("Cliente #%d Ready to receive info ", cliente_num)
    logging.info("CLIENT: client #%d ready to receive info", cliente_num)
    dataTotal = ''

    while True:
        # Message received from server
        data = s.recv(1048576)
        dataTotal += str(data.decode('ANSI'))

        if not data:
            print("Termino el envío")
            break
        elif (data.__contains__(b"HASHH")):
            logging.info("Found hash")
            index = data.find(b"HASHH")

            index2 = dataTotal.find("HASHH")

            m.update(dataTotal[:index2].encode(
                encoding='ANSI', errors='strict'))

            realM = data[index+5:]
            print("Hash recibido ", realM.decode(
                encoding='ANSI', errors='strict'))
            print("Hash creado ", m.hexdigest())
            if m.hexdigest() == realM.decode():
                print("Hash correcto")
                logging.info("CLIENT: hash correcto")
            else:
                print("Hash incorrecto")
                logging.info("CLIENT: hash corrupto ")

    logging.info('CLIENT: Tiempo del envío %s', (time.time()-start_time))
    logging.info("---------------------------------------------")
    s.close()


main()
