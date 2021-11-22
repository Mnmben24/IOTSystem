from Objects import Objects
import tcpserver

ObjServer = None
AppServer = None

def startObjServer(ObjServer):
    ObjServer = tcpserver.ObjectServer()

startObjServer(ObjServer)


