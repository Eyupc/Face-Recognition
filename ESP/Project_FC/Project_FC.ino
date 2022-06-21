#include <WiFi.h>
#include <WebSocketsServer.h>
#include <ArduinoJson.h>

const int PIN_DOOR = 2;
const char* ssid = "telenet-DF7D9FF";
const char* password = "trTv2ahhGumb";

WebSocketsServer webSocket = WebSocketsServer(8888);
void onWebSocketEvent(uint8_t num,
                      WStype_t type,
                      uint8_t * payload,
                      size_t length) {

  // Figure out the type of WebSocket event
  switch(type) {

    // Client has disconnected
    case WStype_DISCONNECTED:
      Serial.printf("[%u] Disconnected!\n", num);
      break;

    // New client has connected
    case WStype_CONNECTED:
      {
        IPAddress ip = webSocket.remoteIP(num);
        Serial.printf("[%u] Connection from ", num);
        Serial.println(ip.toString());
      }
      break;

    case WStype_TEXT:
    {
      Serial.printf("[%u] Text: %s\n", num, payload);
      StaticJsonDocument<200> doc;
      DeserializationError error = deserializeJson(doc, payload);
      JsonObject obj = doc.as<JsonObject>();
      String header = obj["header"].as<String>();
      Serial.println(header);
      if(header == "OpenDoorEvent"){
      JsonArray arr = obj["data"].as<JsonArray>();
      boolean needToOpen = arr[0]["open"].as<boolean>();
      openDoor(needToOpen);
      }
    }         
      break;

    // For everything else: do nothing
    case WStype_BIN:
    case WStype_ERROR:
    case WStype_FRAGMENT_TEXT_START:
    case WStype_FRAGMENT_BIN_START:
    case WStype_FRAGMENT:
    case WStype_FRAGMENT_FIN:
    default:
      break;
  }
}

void setup() {

  pinMode(PIN_DOOR,OUTPUT);
  // Start Serial port
  Serial.begin(115200);

  // Connect to access point
  Serial.println("Connecting");
  WiFi.begin(ssid, password);
  while ( WiFi.status() != WL_CONNECTED ) {
    delay(500);
    Serial.print(".");
  }

  // Print our IP address
  Serial.println("Connected!");
  Serial.print("My IP address: ");
  Serial.println(WiFi.localIP());

  // Start WebSocket server and assign callback
  webSocket.begin();
  webSocket.onEvent(onWebSocketEvent);
}

void loop() {

 // Serial.print(WiFi.localIP());
  webSocket.loop();
}

void openDoor(bool val){
digitalWrite(PIN_DOOR,val);
delay(1000);
digitalWrite(PIN_DOOR,0);
}
