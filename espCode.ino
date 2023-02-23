#include "DHT.h"
#include "FirebaseArduino.h"

// define pin data
#define DHTPIN    2
#define ldrPin    3
#define heaterPin 4
#define fogPin    5
#define shadePin  6
// define firebase data
#define FIREBASE_HOST "https://ieee-paper.firebaseio.com/");
#define FIREBASE_AUTH "AIza"
// define wfifi data
#define WIFI_SSID     "IEEE"
#define WIFI_PASSWORD "IEEE"
// define DHT data
#define DHTTYPE DHT22

// These constants should match the photoresistor's "gamma" and "rl10" attributes
const float GAMMA  = 0.7;
const float RL10   =  50;

// initialise objects
DHT dht(DHTPIN, DHTTYPE);

void setup()
{
    // put your setup code here, to run once:
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
    Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
    //initialise firebase sensor data string vars
    Firebase.setString("humidity",    "0");
    Firebase.setString("temperature", "0");
    Firebase.setString("fahrenheit",  "0");
    Firebase.setString("hic",         "0");
    Firebase.setString("hif",         "0");
    Firebase.setString("lux",         "0");
    //initialise firebase device string vars
    Firebase.setString("FogPump",    "OFF");
    Firebase.setString("ShadeMotor", "OFF");
    Firebase.setString("Heater",     "OFF");
    //initialise vars
    String fireFogPump    = "";
    String fireShadeMotor = "";
    String fireHeater     = "";
    String firetemperature    = "";
    String firehumidity    = "";
    String firelux    = "";


    //begin dht sensor
    dht.begin();

    // set pin mode
    pinMode(ldrPin,     INPUT);
    pinMode(DHTPIN,     INPUT);
    pinMode(heaterPin, OUTPUT);
    pinMode(shadePin,  OUTPUT);
    pinMode(fogPin,    OUTPUT);
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
    float fahrenheit  = dht.readTemperature(true);

    // Check if any reads failed and exit early (to try again).
    if (isnan(humidity) || isnan(temperature) || isnan(fahrenheit))
    {
        Serial.println(F("Failed to read from DHT sensor!"));
        return;
    }

    // Compute heat index in Fahrenheit (the default)
    float hif = dht.computeHeatIndex(fahrenheit, humidity);
    // Compute heat index in Celsius (isFahreheit = false)
    float hic = dht.computeHeatIndex(temperature, humidity, false);

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
    //sending data to firebase
    firetemperature = String(temperature)+String("Celcius");
    firehumidity    = String(humidity)+String("%");
    FireBase.pushString("DHT22/Humidity",firehumidity);
    FireBase.pushString("DHT22/Temperature",firetemperature);
    if (Firebase.failed()){
        Serial.print("pushing dht22/logs failed");
        Serial.println(Firebase.error());
        return;
    }

    /*==============================================================================
    ================================================================================
    ===========================Light================================================
    ================================================================================
    ================================================================================*/
    // Convert the analog value into lux value:
    int analogValue = analogRead(ldrPin);
    float voltage = (analogValue / 1024.) * 5;
    float resistance = 2000 * voltage / (1 - voltage / 5);
    float lux = pow(RL10 * 1e3 * pow(10, GAMMA) / resistance, (1 / GAMMA));

    Serial.println(F("Intensity: "));
    Serial.print(lux);
    Serial.print(F("lux"));
     //sending data to firebase
    firelux = String(lux)+String("lux");
    FireBase.pushString("lightIntensity",firelux);
    if (Firebase.failed()){
        Serial.print("pushing lux/logs failed");
        Serial.println(Firebase.error());
        return;
    }

    /*==============================================================================
    ================================================================================
    ===========================Heater===============================================
    ================================================================================
    ================================================================================*/
    fireHeater = Firebase.getString("Heater",     "OFF");
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
    fireShadeMotor = Firebase.getString("ShadeMotor", "OFF");
    if (fireShadeMotor = "ON"){
        Serial.println("Heater turned on");
        digitalWrite(shadePin,HIGH);
    }else if (fireShadeMotor = "OFF"){
        Serial.println("Heater turned off");
        digitalWrite(shadePin,LOW);
    }else{
        Serial.println("command Error, please send shade ON/OFF")
}
