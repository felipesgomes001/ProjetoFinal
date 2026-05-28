#include <WiFi.h>

const char* ssid = "Steakeholders";
const char* password = "01020304";

// IP FIXO DO CARRINHO
IPAddress local_IP(10, 151, 185, 105);
IPAddress gateway(10, 151, 185, 189);
IPAddress subnet(255, 255, 255, 0);

WiFiServer server(5000);

void setup() {

  Serial.begin(115200);

  WiFi.config(local_IP, gateway, subnet);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println(WiFi.localIP());wsw

  server.begin();
}

void loop() {

  WiFiClient client = server.available();

  if (client) {

    while (client.connected()) {

      if (client.available()) {

        char comando = client.read();

        Serial.print("Recebido: ");
        Serial.println(comando);

        // FRENTE
        if (comando == 'w') {
          Serial.println("Movendo para frente");
        }

        // TRÁS
        if (comando == 's') {
          Serial.println("Movendo para trás");
        }

        // ESQUERDA
        if (comando == 'a') {
          Serial.println("Virando esquerda");
        }

        // DIREITA
        if (comando == 'd') {
          Serial.println("Virando direita");
        }

        // PARAR
        if (comando == 'p') {
          Serial.println("Parando");
        }
      }
    }

    client.stop();
  }
}