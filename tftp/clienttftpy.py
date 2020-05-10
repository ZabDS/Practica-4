
import tftpy
import time
import os

host = "127.0.0.1"
port = 69
output = "xx"
timeout = 5
options = {}

def SubirArchivo(filename):
    try:
        context = tftpy.TftpContexts.TftpContextClientUpload(host, port, output, filename, options, None, timeout)
    except FileNotFoundError:
        print("Archivo no encontrado")
        return -1
    
    print("Enviando WRQ to %s" % context.host)
    context.metrics.start_time = time.time()
        
    pkt = tftpy.TftpPacketTypes.TftpPacketWRQ()
    pkt.filename = context.file_to_transfer
    pkt.mode = "octet"
    pkt.options = context.options
    context.sock.sendto(pkt.encode().buffer, (context.host, context.port))
    context.next_block = 1
    context.last_pkt = pkt
    
    context.state = tftpy.TftpStates.TftpStateSentWRQ(context)
    
    while context.state:
        try:
            print("Estado es: %s" % context.state)
            context.cycle()
        except tftpy.TftpShared.TftpTimeout as err:
            print(str(err))
            context.retry_count += 1
            if context.retry_count >= timeout:
                print("Maximo de intentos alcazados, saliendo")
                return -1
            else:
                print("Reenviando ultimo paquete")
                context.state.resendLast()
    print("Terminando el envío del archivo")
    
def DescargarArchivo(filename):
    context = tftpy.TftpContexts.TftpContextClientDownload(host, port, filename, output, options, None, timeout)
    print("Enviando RRQ to %s" % context.host)
    context.metrics.start_time = time.time()
        
    pkt = tftpy.TftpPacketTypes.TftpPacketRRQ()
    pkt.filename = context.file_to_transfer
    pkt.mode = "octet"
    pkt.options = context.options
    context.sock.sendto(pkt.encode().buffer, (context.host, context.port))
    context.next_block = 1
    context.last_pkt = pkt

    context.state = tftpy.TftpStates.TftpStateSentRRQ(context)
    while context.state:
        try:
            print("Estado es %s" % context.state)
            context.cycle()
        except tftpy.TftpShared.TftpTimeout as err:
            print(str(err))
            context.retry_count += 1
            if context.retry_count >= timeout:
                print("Máximo de intentos alcanzados, saliendo")
                return -1
            else:
                print("Reenviando el ultimo paquete")
                context.state.resendLast()
        except tftpy.TftpShared.TftpFileNotFoundError as err:
            print("No existe el archivo en el servidor")
            if context.fileobj is not None and not context.filelike_fileobj:
                if os.path.exists(context.fileobj.name):
                    print("Desligando el archivo de salida a: %s", context.fileobj.name)
                    os.unlink(context.fileobj.name)
            return -1
    print("Descarga completada")


while True:
    opc = input("Ingrese alguna de las siguientes opciones:\n"
           "1.-Enviar un RRQ\n"
           "2.-Enviar un WRQ\n"
           "3.-Terminar Cliente\n")
    if int(opc) == 1:
        filename = input("Ingrese el nombre del archivo: ")
        DescargarArchivo(filename)
    elif int(opc) == 2:
        filename = input("Ingrese el nombre del archivo: ")
        SubirArchivo(filename)
    elif int(opc) == 3:
        break
    else: 
        print("Elija una opcion válida")
