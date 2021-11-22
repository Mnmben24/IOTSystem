import datetime
import socket

class Objects:

    ID = 0
    Name = ""
    Status = ""
    Type = ""

    def __init__(self, ID, Name, Connection, Type, DefaultStatus="Closed"):
        self.ID = ID
        self.Name = Name
        self.Connection = Connection
        self.Type = Type
        self.Status = DefaultStatus
        self.trigger = False
        self.Connection.settimeout(10)
    
    def Get_Name(self):
        return self.Name
    
    def Set_Name(self, new_value):
        self.Name = new_value

    def Get_Connection(self):
            return self.Connection

    def Set_Connection(self, new_value):
        self.Connection = new_value

    def Get_Type(self):
        return self.Name

    def Get_Status(self):
        return self.Status
    
    def Set_Status(self, new_value):
        self.Status = new_value

    def Trigger(self):
        self.trigger = True
        print("Triggering " + self.Name, datetime.datetime.now())

    def main_loop(self):
        data = "Start"
        while data:
            try:
                data = self.Connection.recv(2048).decode('utf-8')
                data = data.replace("\n","").replace("\r","")
                if data == 'exit':
                    break
                print("Recieved:", data)
                if int(data) == 0:
                    self.Status = "Closed"
                else:
                    self.Status = "Open"
                if self.trigger:
                    self.Connection.send(b'1')
                    self.trigger = False
                    continue
                self.Connection.send(b'0')
            except socket.timeout as ex:
                return None
