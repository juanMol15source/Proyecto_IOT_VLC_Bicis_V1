import requests
import time
import json
import paho.mqtt.client as mqtt

API_URL = "http://api.citybik.es/v2/networks/valenbisi"

MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883
MQTT_TOPIC = "valenbisi/stations"


def main():
    cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    cliente.connect(MQTT_BROKER, MQTT_PORT)
    cliente.loop_start()

    while True:
        estaciones = requests.get(API_URL, timeout=10).json()["network"]["stations"][:100]
        for e in estaciones:

            mensaje = {
                "station": e["name"],
                "free_bikes": e["free_bikes"],
                "empty_slots": e["empty_slots"],
                "latitude": e["latitude"],
                "longitude": e["longitude"]
            }

            cliente.publish(MQTT_TOPIC, json.dumps(mensaje))

            print(f"Estación: {e['name']}\n  Bicicletas libres: {e['free_bikes']}\n  Huecos libres: {e['empty_slots']}\n")

        time.sleep(3)


if __name__ == "__main__":
    main()
