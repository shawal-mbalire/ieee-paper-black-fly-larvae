/*
Shawal Mbalire
IEEE Paper Black Soldier Fly BSF
*/
#include <DHT.h>
#include <Firebase_ESP_Client.h>
#include <WiFi.h>
#include <BH1750.h>
#include <Wire.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"

#define WIFI_SSID     "Shawal_iOS"//"TP-Link_659A"//
#define WIFI_PASSWORD "12121217"//"98781997""98781997"//
#define DATABASE_URL  "https://ieeepaper-default-rtdb.europe-west1.firebasedatabase.app"
#define API_KEY       "AIzaSyAHDUls-v3DKM7q9X70OkXaMzIbNgWqHR4"
#define USER_EMAIL    "esp32s@bsf.com"
#define USER_PASSWORD "password"

#define DHTTYPE   DHT22

#define DHTPIN    19
//#define ldrPin    4
#define heaterPin 18
#define fogPin    19
#define shadePin  2
//#define bh1750_sda 21
//#define bh1750_scl 22


DHT            dht(DHTPIN, DHTTYPE);
BH1750         lightMeter(0x23);
FirebaseData   fbdo;
FirebaseAuth   auth;
FirebaseConfig config;
FirebaseJson   temjson;
FirebaseJson   luxjson;
FirebaseJson   humjson;
WiFiUDP        ntpUDP;
NTPClient      timeClient(ntpUDP);

const float   luxLowerLimit      = 550;
const float   luxHigherLimit     = 10000;
const float   GAMMA              = 0.7;
const float   RL10               = 50;
unsigned long sendDataPrevMillis = 0;
bool          signupOK           = false;
bool          setFog;
bool          setShade;
bool          setBulb;
float         lux;
//float         lux_ldr;
int           splitT;
String        formattedDate;
String        dayStamp;
String        timeStamp;

void setup(){
    pinMode(ldrPin,     INPUT);
    pinMode(DHTPIN,     INPUT);
    pinMode(heaterPin, OUTPUT);
    pinMode(shadePin,  OUTPUT);
    pinMode(fogPin,    OUTPUT);

    dht.begin();
    Wire.begin();
    Serial.begin(115200);
    Serial.println("Hello, Node MCU ESP-32!");
    
    //===========================BH1750====================
    if (lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE)) {
      Serial.println(F("BH1750 Advanced begin"));
    } else {
      Serial.println(F("Error initialising BH1750"));
    }

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


    timeClient.setTimeOffset(3600*3);
    timeClient.begin();

    /*==============================================================================
    ================================================================================
    ===========================FireBase=============================================
    ================================================================================
    ================================================================================*/
    config.api_key     = API_KEY;
    config.database_url= DATABASE_URL;
    auth.user.email    = USER_EMAIL;
    auth.user.password = USER_PASSWORD;

    if (Firebase.signUp(&config,&auth,"","")){
      Serial.println("Sign up ok");
      signupOK = true;
    }else{
      Serial.printf("%s\n",config.signer.signupError.message.c_str());
    }
    config.token_status_callback = tokenStatusCallback;
    Firebase.begin(&config,&auth);
    Firebase.reconnectWiFi(true);
    Firebase.RTDB.enableClassicRequest(&fbdo,true);
}

void loop()
{
    //
    delay(5000);
    /*==============================================================================
    ================================================================================
    ===========================Time================================================
    ================================================================================
    ================================================================================*/
   
    while(!timeClient.update()) {
        timeClient.forceUpdate();
      }
    formattedDate = timeClient.getFormattedDate();
    splitT        = formattedDate.indexOf("T");
    dayStamp      = formattedDate.substring(0, splitT);
    timeStamp     = formattedDate.substring(splitT+1, formattedDate.length()-1);
    /*==============================================================================
    ================================================================================
    ===========================DHT22================================================
    ================================================================================
    ================================================================================*/
    float humidity    = dht.readHumidity();
    float temperature = dht.readTemperature();
    if (isnan(humidity) || isnan(temperature)){
        Serial.println(F("Failed to read from DHT sensor!"));
        return;
    }
    Serial.print(F("Humidity: "));
    Serial.print(humidity);
    Serial.print(F("%  Temperature: "));
    Serial.print(temperature);
    Serial.print(F("°C "));


    temjson.add("day",dayStamp);
    temjson.add("time",timeStamp);
    temjson.add("tem",temperature);


    humjson.add("day",dayStamp);
    humjson.add("time",timeStamp);
    humjson.add("hum",humidity);

    /*==============================================================================
    ================================================================================
    ===========================Light Sensor=========================================
    ================================================================================
    ================================================================================*/

    // Convert the ldr analog value into lux value:
    //float analogValue = analogRead(ldrPin);
    //float voltage     = (analogValue / 1023.) * 5;
    //float resistance  = 2000 * voltage / (1 - voltage / 5);
    //lux_ldr     = pow(RL10 * 1e3 * pow(10, GAMMA) / resistance, (1 / GAMMA));
    //Serial.println(F("Intensity: "));
    //Serial.print(lux_ldr);
    //Serial.print(F("lux"));

    // ==========BH1750=========================
    
    if (lightMeter.measurementReady()) {
      lux = lightMeter.readLightLevel();
      Serial.print("Light: ");
      Serial.print(lux);
      Serial.println(" lx");
    }
     
    luxjson.add("day",dayStamp);
    luxjson.add("time",timeStamp);
    //luxjson.add("lux_ldr",lux_ldr);
    luxjson.add("lux",lux);

    /*==============================================================================
    ================================================================================
    ===========================Heater===============================================
    ================================================================================
    ================================================================================*/
    if (lux < luxLowerLimit):digitalWrite(heaterPin, HIGH)
    if (lux > luxHigherLimit): digitalWrite(heaterPin, LOW)
    if (Firebase.RTDB.getBool(&fbdo, "heaterBulb/setOn")) {
        if (fbdo.dataType() == "boolean") {
            setBulb = fbdo.boolData();
            Serial.println("Successful READ from " + fbdo.dataPath() + ":" + String(setBulb) + " (" + fbdo.dataType() + " ");
            //ledcWrite (PWMChannel, pwmValue);
            digitalWrite(heaterPin, setBulb);
        }
    }else{
        Serial.println("FAILED: " + fbdo.errorReason ());
    }
    /*==============================================================================
    ================================================================================
    ===========================FogPump===============================================
    ================================================================================
    ================================================================================*/
    if (Firebase.RTDB.getBool(&fbdo, "fogMachine/setOn")) {
        if (fbdo.dataType() == "boolean") {
            setFog = fbdo.boolData();
            Serial.println("Successful READ from " + fbdo.dataPath() + ":" + String(setFog) + " (" + fbdo.dataType() + " ");
            //ledcWrite (PWMChannel, pwmValue);
            digitalWrite(fogPin, setFog);
        }
    }else{
        Serial.println("FAILED: " + fbdo.errorReason ());
    }
    /*==============================================================================
    ================================================================================
    ===========================Shade================================================
    ================================================================================
    ================================================================================*/
    if (Firebase.RTDB.getBool(&fbdo, "shadeMotor/setOnn")) {
        if (fbdo.dataType() == "boolean") {
            setShade = fbdo.boolData();
            Serial.println("Successful READ from " + fbdo.dataPath() + ":" + String(setShade) + " (" + fbdo.dataType() + " ");
            //ledcWrite (PWMChannel, pwmValue);
            digitalWrite(shadePin, setShade);
        }
    }else{
        Serial.println("FAILED: " + fbdo.errorReason ());
    }




  if (Firebase.ready() && signupOK && (millis() - sendDataPrevMillis > 15000 || sendDataPrevMillis == 0)){
    sendDataPrevMillis = millis();
    // -----------------STORE sensor data to a RTDB----------------------

    //-------------setting ldr lux data to firebase----------------
    if (Firebase.RTDB.setFloat(&fbdo, "LDR/lux", lux_ldr)){
      Serial.println("LDR LUX SENT");
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println("TYPE: " + fbdo.dataType());
    }else {
      Serial.println("FAILED TO SEND LDR LUX");
      Serial.println("REASON: " + fbdo.errorReason());
    }

    //-------------setting lux data to firebase----------------
    if (Firebase.RTDB.setFloat(&fbdo, "BH1750/lux", lux)){
      Serial.println("BH1750 LUX SENT");
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println("TYPE: " + fbdo.dataType());
    }else {
      Serial.println("FAILED TO SEND BH1750 LUX");
      Serial.println("REASON: " + fbdo.errorReason());
    }

    //-------------setting humidity data to firebase----------------
    if (Firebase.RTDB.setFloat(&fbdo, "DHT/humidity", humidity)){
      Serial.println("HUMIDITY SENT");
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println("TYPE: " + fbdo.dataType());
    }else {
      Serial.println("FAILED TO SEND HUMIDITY");
      Serial.println("REASON: " + fbdo.errorReason());
    }

    //-------------setting temperature data to firebase----------------
    if (Firebase.RTDB.setFloat(&fbdo, "DHT/temperature(celcius)", temperature)){
      Serial.println("TEMPERATURE SENT");
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println("TYPE: " + fbdo.dataType());
    }else {
      Serial.println("FAILED TO SEND TEMPERATURE");
      Serial.println("REASON: " + fbdo.errorReason());
    }

    //-------------setting shade ison data to firebase----------------
    if (Firebase.RTDB.setBool(&fbdo, "shadeMotor/isOn", digitalRead(shadePin))){
      Serial.println("shadeMotor SENT");
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println("TYPE: " + fbdo.dataType());
    }else {
      Serial.println("FAILED TO SEND shadeMotor");
      Serial.println("REASON: " + fbdo.errorReason());
    }

    //-------------setting heater data to firebase----------------
    if (Firebase.RTDB.setBool(&fbdo, "heaterBulb/isOn", digitalRead(heaterPin))){
      Serial.println("heaterBulb SENT");
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println("TYPE: " + fbdo.dataType());
    }else {
      Serial.println("FAILED TO SEND heaterBulb");
      Serial.println("REASON: " + fbdo.errorReason());
    }

    //-------------setting fogMachine data to firebase----------------
    if (Firebase.RTDB.setBool(&fbdo, "fogMachine/isOn", digitalRead(fogPin))){
      Serial.println("fogMachine SENT");
      Serial.println("PATH: " + fbdo.dataPath());
      Serial.println("TYPE: " + fbdo.dataType());
    }else {
      Serial.println("FAILED TO SEND fogMachine");
      Serial.println("REASON: " + fbdo.errorReason());
    }

    //------------------------pushing temp json to graph--------------------
    if (Firebase.RTDB.pushJSON(&fbdo, "graph/temp", &temjson)) {
      Serial.println(fbdo.dataPath());
      Serial.println(fbdo.pushName());
      Serial.println(fbdo.dataPath() + "/"+ fbdo.pushName());
    } else {
      Serial.println(fbdo.errorReason());
    }
    
    //------------------------pushing hum json to graph--------------------
    if (Firebase.RTDB.pushJSON(&fbdo, "graph/hum", &humjson)) {
      Serial.println(fbdo.dataPath());
      Serial.println(fbdo.pushName());
      Serial.println(fbdo.dataPath() + "/"+ fbdo.pushName());
    } else {
      Serial.println(fbdo.errorReason());
    }

    //------------------------pushing lux json to graph--------------------
    if (Firebase.RTDB.pushJSON(&fbdo, "graph/lux", &luxjson)) {
      Serial.println(fbdo.dataPath());
      Serial.println(fbdo.pushName());
      Serial.println(fbdo.dataPath() + "/"+ fbdo.pushName());
    } else {
      Serial.println(fbdo.errorReason());
    }
}
}
