import tftpy
import os

host = "127.0.0.1"
port = 69
filename = "prueba.txt"
output = "xx"
timeout = 5



root = os.path.dirname(os.path.abspath("prueba.txt"))

server = tftpy.TftpServer(root)
server.listen(host, port)


