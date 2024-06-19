#include <M5StickCPlus.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLE2902.h>

#define SERVICE_UUID "eb6b6d8c-f17f-45e0-940a-b7864d850353"
#define CHARACTERISTIC_UUID "b0bb55cf-e0f0-4b05-8bca-c6a5835c7a02"

BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = false;
bool advertising = false;
int num = 0;
const int BTNA = 37;
int waitingForRelease = 1;
int pressCount = 0;

class MyServerCallbacks: public BLEServerCallbacks {
  void onConnect(BLEServer* pServer, esp_ble_gatts_cb_param_t *param) {
    Serial.println("Device Connected");
    M5.Lcd.print("Connected");
    deviceConnected = true;
    advertising = false;
  };

  void onDisconnect(BLEServer* pServer) {
    Serial.println("Device Disconnected");
    deviceConnected = false;
  }
};

void setup() {
  M5.begin();
  M5.Imu.Init();
  
  BLEDevice::init("M5StickCPlus-Seth");
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  BLEService *pService = pServer->createService(SERVICE_UUID);
  pCharacteristic = pService->createCharacteristic(
    CHARACTERISTIC_UUID,
    BLECharacteristic::PROPERTY_READ |
    BLECharacteristic::PROPERTY_NOTIFY
  );
  pCharacteristic->addDescriptor(new BLE2902());
  pService->start();
  BLEDevice::startAdvertising();
}

#pragma pack(1)
typedef struct {
  uint16_t button;
  uint16_t count;
} Packet; 


void ButtonPress() { 
  Packet p;
  p.button = waitingForRelease;
  p.count = pressCount;
  pCharacteristic->setValue((uint8_t*)&p, sizeof(Packet));
}
int previous = 0;

void loop() {
  if (deviceConnected) {
    
    if(digitalRead(BTNA)==LOW && !waitingForRelease){

      if(previous==0){
        pressCount = pressCount + 1;
      }
      waitingForRelease = 1;
      previous = waitingForRelease;
    }
    if(digitalRead(BTNA)==HIGH) {
      waitingForRelease = 0;
      previous = waitingForRelease;
    }
    
    ButtonPress();
    pCharacteristic->notify();
    num++;
    delay(10);

  }
  if(!deviceConnected && !advertising) {
    BLEDevice::startAdvertising();
    M5.Lcd.fillScreen(BLACK);
    M5.Lcd.print("Advertising");
    Serial.println("Start Advertising");
    pressCount = 0;
    advertising = true;    
    delay(10);
  }
  
}
