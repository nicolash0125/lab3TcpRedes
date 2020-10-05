# IMPORTS
import socket
import os
import logging
import datetime
import hashlib

HOST = '127.0.0.1'
port = 65430

newFile = ''
path = ''
# LOGGER
# Create and configure logger
logging.basicConfig(filename="serverLogger" + datetime.date.today().strftime("%B %d, %Y") + ".log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
# Creating an object
logger = logging.getLogger()
# Setting the threshold of logger to INFO
logger.setLevel(logging.INFO)

# INPUTS DE CONFIGURACIÓN
while True:
    # 2. Tener dos archivos disponibles para su envío a los clientes: un archivo de tamaño 100 MiB, y otro de 250 MiB. Se sugiera que uno de estos archivos sea multimedia.
    # 3. La aplicación debe permitir seleccionar qué archivo desea enviarse a los clientes conectados y a cuántos clientes en simultáneo.


    selectedFile = input('Escoje un archivo')

    if selectedFile == '1':
        newFile = '../videos/1.txt'
        path = '../videos/'
        break
    elif selectedFile == '2':
        newFile = '../videos/2.txt'
        path = './archivos/'
        break


# Calcular el Hash
def getmd5file(archivo):
    try:
        hashmd5 = hashlib.md5()
        with open(archivo, "rb") as f:
            for bloque in iter(lambda: f.read(4096), b""):
                hashmd5.update(bloque)
        return hashmd5.hexdigest()
    except Exception as e:
        print("Error: %s" % (e))
        return ""
    except:
        print("Error desconocido")
        return ""


hashCalculado = getmd5file(newFile)
nombreHash = "hash" + selectedFile + ".txt"
hashfile = open((path + nombreHash), "w+")
if os.stat(path + nombreHash).st_size == 0:
    hashfile.write(hashCalculado)
hashfile.close()

pool = 0
while True:
    selectedPool = int(input('Select number of people to send the file (Max 25): '))
    if selectedPool > 0 and selectedPool < 26:
        pool = selectedPool
        break

print('Pool of ' + str(pool) + ' clients')
print('Selected File to transfer: ' + newFile)

# PROTOCOLO
# Creación del Socket: Puerto e IP
# Reserve a port for your service every new transfer wants a new port or you must wait.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
host = socket.gethostname()  # Get local machine name
s.bind((host, port))  # Bind to the port
s.listen(selectedPool)  # Now wait for client connection.

print('Server: listening....')

poolCounter = 0
while True:
    # 1. Recibir conexiones TCP. La aplicación debe soportar 25 conexiones en simultáneo.
    server, addr = s.accept()  # Establish connection with client.
    poolCounter = poolCounter + 1
    print('Server: Got connection from', addr)
    print('Server: There are ' + str(poolCounter) + ' client(s) connected')
    print('Server: You need ' + str(pool) + ' to send the file')
    if poolCounter == pool:

        # 4. Realizar la transferencia de archivos a los clientes definidos en la prueba.
        directory = os.listdir(path)
        for files in directory:
            print(files)
            filename = files
            size = len(filename)
            size = bin(size)[2:].zfill(16)  # encode filename size as 16 bit binary
            server.send(size.encode())
            server.send(filename.encode())

            filename = os.path.join(path, filename)
            filesize = os.path.getsize(filename)
            filesize = bin(filesize)[2:].zfill(32)  # encode filesize as 32 bit binary
            server.send(filesize.encode())

            file_to_send = open(filename, 'rb')

            l = file_to_send.read()
            server.sendall(l)
            file_to_send.close()
            print('File Sent')

# 6. La aplicación debe permitir medir el tiempo de transferencia de un archivo en segundos.
# Al final de cada transferencia la aplicación debe reportar si el archivo está completo y
# correcto y el tiempo total de transferencia, para esto genere un log para cada intercambio de
# datos entre cliente y servidor.
# 7. Disponer un repositorio de los archivos recibidos y logs. (Revisar sección de recomendaciones).


# server.close()
#  break
