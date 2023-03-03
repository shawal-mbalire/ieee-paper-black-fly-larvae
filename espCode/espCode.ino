/*
Shawal Mbalire
IEEE Paper Black Soldier Fly BSF
*/
#include <DHT.h>
#include <Firebase_ESP_Client.h>
#include <WiFi.h>
#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"

#define WIFI_SSID     "TP-Link_659A"
#define WIFI_PASSWORD "98781997"
#define DATABASE_URL "https://ieeepaper-default-rtdb.europe-west1.firebasedatabase.app");
#define API_KEY "AIzaSyAHDUls-v3DKM7q9X70OkXaMzIbNgWqHR4"

#define DHTTYPE   DHT22
#define DHTPIN    2
#define ldrPin    3
#define heaterPin 4
#define fogPin    5
#define shadePin  6

DHT dht(DHTPIN, DHTTYPE);
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

const float   GAMMA              = 0.7;
const float   RL10               = 50;
unsigned long sendDataPrevMillis = 0;
bool          signupOK           = false;
float         firetemperature    = "";
float         firehumidity       = "";
int           firelux            = "";
String        fireFogPump        = "";
String        fireShadeMotor     = "";
String        fireHeater         = "";


void setup(){
    pinMode(ldrPin,     INPUT);
    pinMode(DHTPIN,     INPUT);
    pinMode(heaterPin, OUTPUT);
    pinMode(shadePin,  OUTPUT);
    pinMode(fogPin,    OUTPUT);
    dht.begin();
    Serial.begin(115200);
    Serial.println("Hello, Node MCU ESP-32!");

    /*==============================================================================
    ================================================================================
    ===========================Wifi================================================
    ================================================================================
    ================================================================================*/
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }
    Serial.println();
    Serial.print("Connected to the ");
    Serial.print(WIFI_SSID);
    Serial.print("WiFi network, IP address: ");
    Serial.println(WiFi.localIP());

    /*==============================================================================
    ================================================================================
    ===========================FireBase=============================================
    ================================================================================
    ================================================================================*/
    config.api_key = API_KEY;
    config.database_url=DATABASE_URL;
    if {Firebase.signUp(&config,&auth,"","")}{
      Serial.println("Sign up ok");
      signupOK = true;
    }else{
      Serial.printf("%s\n",config.signer.signupError.message.c_str());
    }
    config.token_status_callback = tokenStatusCallback;
    Firebase.begin(&config,&auth);
    Firebase.reconnectWiFi(true);
}

void loop()
{
    //
    delay(5000);

    /*==============================================================================
    ================================================================================
    ===========================DHT22================================================
    ================================================================================
    ================================================================================*/
    float humidity    = dht.readHumidity();
    float temperature = dht.readTemperature();
    if (isnan(humidity) || isnan(temperature) || isnan(fahrenheit)){
        Serial.println(F("Failed to read from DHT sensor!"));
        return;
    }
    Serial.print(F("Humidity: "));
    Serial.print(humidity);
    Serial.print(F("%  Temperature: "));
    Serial.print(temperature);
    Serial.print(F("°C "));
    Serial.print(fahrenheit);
    Serial.print(F("°F  Heat index: "));
    Serial.print(hic);
    Serial.print(F("°C "));
    Serial.print(hif);
    Serial.println(F("°F"));

    /*==============================================================================
    ================================================================================
    ===========================Light================================================
    ================================================================================
    ================================================================================*/
    // Convert the analog value into lux value:
    int   analogValue = analogRead(ldrPin);
    float voltage     = (analogValue / 1024.) * 5;
    float resistance  = 2000 * voltage / (1 - voltage / 5);
    float lux         = pow(RL10 * 1e3 * pow(10, GAMMA) / resistance, (1 / GAMMA));
    Serial.println(F("Intensity: "));
    Serial.print(lux);
    Serial.print(F("lux"));


    /*==============================================================================
    ================================================================================
    ===========================Heater===============================================
    ================================================================================
    ================================================================================*/
    fireHeater = Firebase.getString("Heater");
    if (fireHeater = "ON"){
        Serial.println("Heater turned on");
        digitalWrite(heaterPin,HIGH);
    }else if (fireHeater = "OFF"){
        Serial.println("Heater turned off");
        digitalWrite(heaterPin,LOW);
    }else{
        Serial.println("command Error, please send fog ON/OFF")
    }
    /*==============================================================================
    ================================================================================
    ===========================FogPump===============================================
    ================================================================================
    ================================================================================*/
    fireFogPump = Firebase.getString("FogPump",    "OFF");
    if (fireFogPump = "ON"){
        Serial.println("Heater turned on");
        digitalWrite(fogPin,HIGH);
    }else if (fireFogPump = "OFF"){
        Serial.println("Heater turned off");
        digitalWrite(fogPin,LOW);
    }else{
        Serial.println("command Error, please send fog ON/OFF")
    /*==============================================================================
    ================================================================================
    ===========================Shade================================================
    ================================================================================
    ================================================================================*/
    if (Firebase.RTDB.getBool(&fbdo, "shadeMotor/setShadeOff")) {
        if (fbdo.dataType ()"bool") {
            shadeValue = fbdo.boolData();
            Serial.println("Successful READ from " + fbdo.dataPath() + ":" + shadeValue + " (" + fbdo.dataType() + " ");
            //ledcWrite (PWMChannel, pwmValue);
            digitalWrite(shadePin, shadeValue);
        }
    }else{
        Serial.println("FAILED: " + fbdo.errorReason ());
    }

    if (fireShadeMotor = "ON"){
        Serial.println("Heater turned on");
        digitalWrite(shadePin,HIGH);
    }else if (fireShadeMotor = "OFF"){
        Serial.println("Heater turned off");
        digitalWrite(shadePin,LOW);
    }else{
        Serial.println("command Error, please send shade ON/OFF")




  if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 15000 || sendDataPrevMillis == 0)){
    sendDataPrevMillis =` millis();
    // -----------------STORE sensor data to a RTDB----------------------
    //-------------pushing lux data to firebase----------------
    if (Firebase.RTDB.setInt(&fbdo, "BH1750/lux", lux)){
      Serial.println("LUX SENT");
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println("TYPE: " + fbdo.dataType());
    }else {
      Serial.println("FAILED TO SEND LUX");
      Serial.println("REASON: " + fbdo.errorReason());
    }
    //-------------pushing humidity data to firebase----------------
    if (Firebase.RTDB.setFloat(&fbdo, "DHT22/humidity", humidity)){
      Serial.println("HUMIDITY SENT");
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println("TYPE: " + fbdo.dataType());
    }else {
      Serial.println("FAILED TO SEND HUMIDITY");
      Serial.println("REASON: " + fbdo.errorReason());
    }
    //-------------pushing temperature data to firebase----------------
    if (Firebase.RTDB.setFloat(&fbdo, "DHT22/temperature(celcius)", temperature)){
      Serial.println("TEMPERATURE SENT");
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println("TYPE: " + fbdo.dataType());
    }else {
      Serial.println("FAILED TO SEND TEMPERATURE");
      Serial.println("REASON: " + fbdo.errorReason());
    }
  }
}
