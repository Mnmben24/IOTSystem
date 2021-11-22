from Objects import Objects
import tcpserver
from _thread import *

ObjServer = None
AppServer = None

def startObjServer(ObjServer):
    ObjServer = tcpserver.ObjectServer()



startObjServer(ObjServer)
#start_new_thread(startObjServer, (ObjServer,))
#start_new_thread(startAppServer, (AppServer, ObjServer))


