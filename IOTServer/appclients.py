import json
import time
import socket

class AppClient:

    def __init__(self, conn):
        self.Connection = conn

    def main_loop(self, objs):
        try:
            self.objs = objs
            send_names = "["
            for obj in self.objs:
                    send_names += obj.Get_Name() + ","
            data = send_names + "]\n"
            print(data)
            self.Connection.send(data.encode('utf-8'))
            while data:
                send_data = {}
                data = self.Connection.recv(2048).decode('utf-8').replace("'",'"').replace("\n","")
                if data == '':
                    break
                rData = json.loads(data)
                print(data)
                if not rData['Name'] == 'None':
                    for obj in self.objs:
                        if obj.Get_Name() == rData['Name']:
                            obj.Trigger()
                for obj in self.objs:
                    send_data[obj.Get_Name()] =  obj.Get_Status()
                self.Connection.send((json.dumps(send_data)+"\n").encode('utf-8'))
                time.sleep(0.5)

            self.Connection.close()
        except socket.timeout as ex:
            return None
        # except socket.reset as ex:
        #     return None

