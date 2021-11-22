
#include <ESP8266WiFi.h>

#include <WiFiManager.h>         // https://github.com/tzapu/WiFiManager


#define Status_Pin 4
#define Relay_Pin 5

int port = 8123;
String host = "192.168.68.118";


int device_status = 0;

WiFiManager wifiManager;
// Use WiFiClient class to create TCP connections
WiFiClient client;

void ConnectToServer(){
  Serial.println("Connecting to Server");
  while (!client.connect(host, port)){
    Serial.println("connection failed");
    delay(5000);
  }
  Serial.println("Connected to Server");
  client.println("{'Name': 'Garage', 'Type': 'OnOffStatus'}");
}

void CloseServerConn(){
  // Close the connection
  Serial.println();
  Serial.println("closing connection");
  client.stop();
}

void Trigger_Relay() {
  digitalWrite(Relay_Pin, HIGH);
  delay(100);
  digitalWrite(Relay_Pin, LOW);
}

void setup() {
  Serial.begin(115200);

  pinMode(Status_Pin, INPUT);
  pinMode(Relay_Pin, OUTPUT);

  digitalWrite(Relay_Pin, LOW);
  
  WiFiServer server(port);
  
  // Uncomment and run it once, if you want to erase all the stored information
  // wifiManager.resetSettings();

  wifiManager.autoConnect("SmartHome");
  
  Serial.println("Connected to Network");

  ConnectToServer();
  
}

void loop(){
  device_status = digitalRead(Status_Pin);
    Serial.println("Status: " + String(device_status));
  if (client.connected()){
    Serial.println("Sending...");
    client.print(device_status);
    while (!client.available())  {delay(10);}
    String line = client.readStringUntil('\n');
    Serial.println("Recieved " + line);
    if (line == "1") {
      Trigger_Relay();
    }
  }
  else{
    ConnectToServer();
  }
}
