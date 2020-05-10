import tftpy
import os

host = "192.168.15.11"
port = 69
filename = "prueba.txt"
output = "xx"
timeout = 5



root = os.path.dirname(os.path.abspath("prueba.txt"))
server = tftpy.TftpServer(root)
print("Iniciando servidor")
print("Esperando petciones tftp..")
server.listen(host, port)


