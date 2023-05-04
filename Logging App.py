import paho.mqtt.client as mqtt
import time

# Connecting to the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to MQTT broker.")
    else:
        print("Connection to MQTT broker failed. Error code: " + str(rc))

# Disconnecting from the MQTT broker
def on_disconnect(client, userdata, rc):
    print("Connection lost at " + time.strftime('%Y-%m-%d %H:%M:%S'))
    # Pause for 5 seconds before reconnecting
    time.sleep(5)
    # Reconnecting to the MQTT broker
    client.reconnect()

# Sending network statistics to the MQTT topic
def statistics(client, disconnect_time, retries):
    message = "Connection was lost at: " + disconnect_time + "\n Reconnected at: " + time.strftime('%Y-%m-%d %H:%M:%S') + "\nNumber of retries: " + str(retries)
    client.publish("/stats/health/device_id/network", message)

def main():
    # Creating a new MQTT client instance
    client = mqtt.Client()
    # Event handlers for connecting and disconnecting
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    # Connecting to the MQTT broker
    client.connect("broker.emqx.io", 1883)

    # Initializing the retry counter to 0
    retries = 0
    while True:
        # Processing incoming MQTT messages and network traffic
        client.loop()
        # Checking if the client is disconnected from the MQTT broker. If disconnected, increment the retries counter
        if not client.is_connected():
            retries += 1
        else:
            # If reconnected after one or more retries
            if retries > 0:
                # Sending network statistics 
                statistics(client, last_disconnected_time, retries)
                # Resetting the retry counter to 0
                retries = 0
            # Recording the time of the last successful connection
            last_disconnected_time = time.strftime('%Y-%m-%d %H:%M:%S')
        # Pause for 1 second before checking the connection again
        time.sleep(1)

if __name__ == "__main__":
    main()