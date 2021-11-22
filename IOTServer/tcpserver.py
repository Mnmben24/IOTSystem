from Objects import Objects
import socket
import os
import json
from _thread import *
from appclients import AppClient

class ObjectServer:
    
    ServerSocket = socket.socket()

    host = "192.168.68.118"
    port = 8123
    
    ThreadCount = 0  
    Objs = []
    AppClients = []

    def __init__(self):
        try:
            self.ServerSocket.bind((self.host, self.port))

            print('Waitiing for a Connection...')
            self.ServerSocket.listen(5)
            while True:
                Client, address = self.ServerSocket.accept()
                print('Client Connected...')
                start_new_thread(self.threaded_client, (Client, ))
                self.ThreadCount += 1

        except socket.error as e:
            print(str(e))

        finally:
            self.close()

    def close(self):
        self.ServerSocket.close()


    def threaded_client(self, connection):
        data = connection.recv(2048).decode('utf-8').replace("'", '"').replace("\n","")
        rData = json.loads(data)
        try:
            if rData['Type'] == "AppClient":
                newObj = AppClient(connection)
                print('New App Device Connected')
                self.AppClients.append(newObj)
                newObj.main_loop(self.Objs)
                self.AppClients.remove(newObj)
                connection.close()
                del newObj
                print("App Client Disconnected")
            else:
                newObj = Objects(self.ThreadCount, rData['Name'], connection, rData['Type'])
                print('Connected to: ' + newObj.Get_Name(), "Status: " + newObj.Get_Status())
                self.Objs.append(newObj)
                newObj.main_loop()
                self.Objs.remove(newObj)
                connection.close()
                del newObj
                print("IOT Client Disconnected")
                
        except error as ex:
            print(ex.toString())
    
    def findClient(self, Name):
        for obj in self.Objs:
            if obj.Get_Name() == Name:
                return obj
        return None

    def triggerClient(self, Name):
        self.findClient(Name).trigger()

    

