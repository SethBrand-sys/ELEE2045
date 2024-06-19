

//WIFI variables defined for setup and initialization

#include <WiFi.h>
#include "esp_wpa2.h"
#include <M5StickCPlus.h>
#define EAP_ANONYMOUS_IDENTITY ""
#define EAP_IDENTITY "swb15837@uga.edu"
#define EAP_PASSWORD "Sammie@321"
#define WPA_PASSWORD "GoDawgs255"
//#define USE_EAP 




int status = 0;
int r = 0;
int g = 0;
int b = 0;

const int BTNA = 37;
#ifdef USE_EAP
  const char* ssid = "eduroam";
#else
  const char* ssid = "WhiteSky-TheConnectionAthens";
#endif

//MQTT included and base values defined
#include <ArduinoMqttClient.h>
const char broker[] = "test.mosquitto.org";
int port = 1883;
WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);
const char light_control_color[] = "elee2045sp23/811899823/light_control_color";
const char light_control_status[] = "elee2045sp23/811899823/light_control_status";
const char topic_status[] = "elee2045sp23/811899823/light_status";



uint16_t rgb565(uint8_t r, uint8_t g, uint8_t b) {
  return ((r / 8) << 11) | ((g / 4) << 5) | (b / 8);
}




void setup() {
  M5.begin();
  M5.Lcd.fillScreen(BLACK);
  WiFi.disconnect(true); //disconnect from wifi to set new wifi connection
  WiFi.mode(WIFI_STA); //init wifi mode
  Serial.flush();
  M5.Axp.ScreenBreath(15);
  RTC_TimeTypeDef TimeStruct;
  M5.Rtc.GetTime(&TimeStruct);
  randomSeed(TimeStruct.Seconds);
  #ifdef USE_EAP
    esp_wifi_sta_wpa2_ent_set_identity((uint8_t *)EAP_ANONYMOUS_IDENTITY, strlen(EAP_ANONYMOUS_IDENTITY));
    esp_wifi_sta_wpa2_ent_set_username((uint8_t *)EAP_IDENTITY, strlen(EAP_IDENTITY));
    esp_wifi_sta_wpa2_ent_set_password((uint8_t *)EAP_PASSWORD, strlen(EAP_PASSWORD));
    esp_wifi_sta_wpa2_ent_enable();
    WiFi.begin(ssid);
  #else
    WiFi.begin(ssid,WPA_PASSWORD);
  #endif
  WiFi.setSleep(false);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Waiting for connection");
  }
  IPAddress ip = WiFi.localIP();
  Serial.println(ip);
  M5.Lcd.print(ip);


//added after connected in setup loop above (just to group it together in a neat way)
  mqttClient.onMessage(onPythonMessage);
  mqttClient.connect(broker, port);
  mqttClient.subscribe(light_control_color);
  mqttClient.subscribe(light_control_status);
  mqttClient.subscribe(topic_status);


}
char buffer[100];
int dif(const char* string1, const char* string2) {
  int i, count = 0;
  int shorter = strlen(string1) < strlen(string2) ? strlen(string1) : strlen(string2);
  for (i = 0; i < shorter; i++) {
    if (string1[i] != string2[i]) {
      count = count + 1;
    }
  }
}


void onPythonMessage(int messageSize) {
  Serial.print(mqttClient.messageTopic());
  mqttClient.read((byte *)buffer,messageSize);
  buffer[messageSize] = 0;
  Serial.println(buffer);
  Serial.println();
  
  
}

void updateStatus() {
  M5.Axp.ScreenBreath(status?15:0);
  M5.Lcd.fillScreen(rgb565(r,g,b));  
}

void sendStatus() {
  mqttClient.beginMessage(topic_status); //begin message in controller color
  mqttClient.write(status);
  mqttClient.write(r);
  mqttClient.write(g);
  mqttClient.write(b);
  mqttClient.endMessage(); //end message in controller color
}



long last_time;
int waitingForRelease = 0;
void loop() {
  mqttClient.poll();
  
  if(millis()-last_time > 2000){
    sendStatus();
    last_time = millis();
  }
  
  if(digitalRead(BTNA)==LOW && !waitingForRelease){
    status = !status;
    updateStatus();
    sendStatus();
    waitingForRelease = 1;
  }
  
  if(digitalRead(BTNA)==HIGH){
    waitingForRelease = 0;
  }
}