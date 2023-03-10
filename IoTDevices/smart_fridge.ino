#include <WiFi.h>

#include <ESP32Ping.h>  /*including the ping library*/

const char* ssid = "TtTAnakin"; /*Define network SSID*/

const char* password = "mitko123"; /*Define Network Password*/

//// Set your Static IP address
//IPAddress local_IP(192, 168, 1, 184);
//// Set your Gateway IP address
//IPAddress gateway(192, 168, 5, 1);
//
//IPAddress subnet(255, 255, 0, 0);
//IPAddress primaryDNS(8, 8, 8, 8);   //optional`
//IPAddress secondaryDNS(8, 8, 4, 4); //optional

void setup() {

  Serial.begin(115200);  /*Baud rate for serial communication*/

  WiFi.begin(ssid, password);  /*Begin WiFi connection*/

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);

    Serial.println("Connecting to WiFi...");


  }



}

void loop() {
  Serial.println(WiFi.localIP());

  bool success = Ping.ping("8.8.8.8", 3);  /*ping ESP32 using google*/
  success = Ping.ping("1.1.1.1", 3);  /*ping ESP32 using google*/
  //success = Ping.ping("www.instagram.com", 3);  /*ping ESP32 using google*/
  //success = Ping.ping("www.alo.bg", 3);  /*ping ESP32 using google*/
  //success = Ping.ping("www.bg-mamma.com", 3);  /*ping ESP32 using google*/
  // success = Ping.ping("www.bg-mamma.com", 3);  /*ping ESP32 using google*/

  if (!success) {

    Serial.println("Ping failed");

    return;

  }
  Serial.println("Ping successful.");
  delay(1500);
}
