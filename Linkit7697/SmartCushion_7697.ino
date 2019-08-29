#include <LWiFi.h>
#include <PubSubClient.h>

char ssid[] = "Fuckpeter";
char password[] = "peterfuck";
char mqtt_server[] = "iot.cht.com.tw";
char sub_topic[] = "/v1/device/18351487392/sensor/input/csv";
char pub_topic[] = "/v1/device/18351487392/rawdata";
char API[] = "PKBJ3AAWY7IRBMUKAH";
char client_Id[] = "linkit-7697";

const int usr_btn = 6; // USR BTN pin is P6
const int relay = 7;

int pub_status = 0;

 
int status = WL_IDLE_STATUS;

WiFiClient mtclient;     
PubSubClient client(mtclient);
long lastMsg = 0;
char msg[256];
int value = 0;

void setup() {
    //Initialize serial and wait for port to open:
    Serial.begin(9600);
    //while (!Serial) {
         // wait for serial port to connect. Needed for native USB port only
    //}
    //attachInterrupt(usr_btn, pin_change, RISING); 
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(relay, OUTPUT);
    pinMode(usr_btn, INPUT);
    setup_wifi();
    client.setServer(mqtt_server, 1883);
    client.setCallback(on_recv);
}
bool sent = false;
int stat = 0;
void loop() {
  if(digitalRead(usr_btn) == HIGH){
    if(sent == false){
      char msg[60];
      sprintf(msg,  "[{\"id\":\"output\",\"value\":[\"%d\"]}]", stat);
      Serial.println(msg);
      if(client.publish(pub_topic, msg)){
        Serial.println("Published!");
        stat = !stat;
      }
      sent = true;
    }
  }
  else{
    sent = false;
  }
  if (!client.connected()) {
    reconnect();
  }
  else{
    client.loop();
  } 
 
}


void printWifiStatus() {              //print Wifi status
    // print the SSID of the network you're attached to:
    Serial.print("SSID: ");
    Serial.println(WiFi.SSID());

    // print your WiFi shield's IP address:
    IPAddress ip = WiFi.localIP();
    Serial.print("IP Address: ");
    Serial.println(ip);

    // print the received signal strength:
    long rssi = WiFi.RSSI();
    Serial.print("signal strength (RSSI):");
    Serial.print(rssi);
    Serial.println(" dBm");
}

void setup_wifi() {                       //setup Wifi
   // attempt to connect to Wifi network:
   Serial.print("Attempting to connect to SSID: ");
   Serial.println(ssid);
   WiFi.begin(ssid, password);
   while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.print(".");
    }
    randomSeed(micros());
    Serial.println("Connected to wifi");
    printWifiStatus();
}

void on_recv(char* topic, byte* payload, unsigned int length) {   //MQTT sub
  Serial.println("Input Message arrived");
  Serial.print("Message: ");
  Serial.println((char*)payload);
  int signal = atoi((char*)payload + length - 1);
  Serial.println(signal);
  if(signal == 1){
    digitalWrite(LED_BUILTIN, HIGH);
    digitalWrite(relay, HIGH);
  }
  else{
    digitalWrite(LED_BUILTIN, LOW);
    digitalWrite(relay, LOW);
  }
  memset(payload, '\0', length);
  
}

void reconnect() {  //reconnect MQTT
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = client_Id;
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str(), API, API)) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      // ... and resubscribe
      client.subscribe(sub_topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
