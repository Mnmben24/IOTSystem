
#include <ESP8266WiFi.h>

#include <WiFiManager.h>         // https://github.com/tzapu/WiFiManager


#define SendKey 0

int port = 8123;
String host = "192.168.68.118";

WiFiManager wifiManager;
// Use WiFiClient class to create TCP connections
WiFiClient client;

void setup() {
  Serial.begin(115200);
  
  WiFiServer server(port);

  
  
  // Uncomment and run it once, if you want to erase all the stored information
  // wifiManager.resetSettings();

  wifiManager.autoConnect("SmartHome");
  
  Serial.println("Connected.");

  while (!client.connect(host, port)) {
    Serial.println("connection failed");
    delay(5000);
  }
}

void loop(){

  

  // This will send a string to the server
  Serial.println("sending data to server");
  if (client.connected()) {
    client.println("{'Name': 'Garage', 'Type': 'OnOffStatus'}");
  }
  else {
    Serial.println("Connecting to the Server");
    if (client.connect(host, port)){
      Serial.println("Connection Failed");
      delay(5000);
    }
  }

  while (client.available() == 0) {}
  char ch = static_cast<char>(client.read());
  Serial.print(ch);

  // Close the connection
  Serial.println();
  Serial.println("closing connection");
  client.stop();

}
