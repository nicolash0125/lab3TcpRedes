# IMPORTS
import socket  # Import socket module
import logging
import datetime
import hashlib

# LOGGER
# Create and configure logger
logging.basicConfig(filename="clientLogger" + datetime.date.today().strftime("%B %d, %Y") + ".log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
# Creating an object
logger = logging.getLogger()
# Setting the threshold of logger to INFO
logger.setLevel(logging.INFO)

# PROTOCOLO
# Creación del Socket: Puerto e IP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
host = '127.0.0.1'  # Ip address that the TCPServer  is there
port = 65430  # Reserve a port for your service every new transfer wants a new port or you must wait.
# 1. Conectarse al servidor TCP y mostrar que se ha realizado dicha conexión. Mostrar el estado de la conexión.
host = socket.gethostname()  # Get local machine name
s.connect((host, port))
print('me conecto')
# 2. Enviar notificación de preparado para recibir datos de parte del servidor.
s.send("Cliente: Hello server!".encode())
print('Hello')
hashCalculado = ''
hashRecibido = ''


# Calcular el nuevo Hash
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


# 3. Recibir un archivo del servidor por medio de una comunicación a través de sockets TCP.
# 3.5 Recibir el Hash
for i in range(2):
    size = s.recv(16).decode()  # Note that you limit your filename length to 255 bytes.
    if not size:
        break
    size = int(size, 2)
    filename = s.recv(size).decode()
    filesize = s.recv(32).decode()
    filesize = int(filesize, 2)
    file_to_write = open(filename)
    chunksize = 4096
    while filesize > 0:
        if filesize < chunksize:
            chunksize = filesize
        data = s.recv(chunksize)
        file_to_write.write(data.decode())
        filesize -= len(data)

    if ('archivo' in filename):
        hashCalculado = getmd5file(filename)
    else:
        hashRecibido = file_to_write.read()
    print('File' + filename + ' received successfully')
    file_to_write.close()
# 4. Verificar la integridad del archivo con respeto a la información entregada por el servidor.
print('Hash Calculado' + hashCalculado)
print('Hash Recibido' + hashRecibido)
if hashCalculado == hashRecibido:
    print('Los Hash Coinciden: Archivo recibido correctamente')
else:
    print('Los Hash no Coinciden: Archivo recibido incorrectamente')

# 5. Enviar notificación de recepción del archivo al servidor
s.send("Cliente: Recibí el archivo!".encode())
# 6. La aplicación debe permitir medir el tiempo de transferencia de un archivo en segundos.
# Al final de cada transferencia la aplicación debe reportar si el archivo está completo y
# correcto y el tiempo total de transferencia, para esto genere un log para cada intercambio de
# datos entre cliente y servidor.
# 7. Disponer un repositorio de los archivos recibidos y logs. (Revisar sección de recomendaciones).

s.close()
print('Client: connection closed')
