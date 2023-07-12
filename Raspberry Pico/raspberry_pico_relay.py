import network
import time
from machine import Pin
from mqtt.simple import MQTTClient
import machine
import uos
import utime


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("open_plotter", "password")  # Anpassa med ditt eget SSID och lösenord
time.sleep(5)
print(wlan.isconnected())
print(wlan.ifconfig())


#LED_PIN = 27

RELAY_OUT1 = 27
RELAY_OUT2 = 26
RELAY_OUT3 = 22
RELAY_OUT4 = 28
RELAY_OUT5 = 19
RELAY_OUT6 = 18

relay_out1 = Pin(RELAY_OUT1, Pin.OUT)
relay_out2 = Pin(RELAY_OUT2, Pin.OUT)
relay_out3 = Pin(RELAY_OUT3, Pin.OUT)
relay_out4 = Pin(RELAY_OUT4, Pin.OUT)
relay_out5 = Pin(RELAY_OUT5, Pin.OUT)
relay_out6 = Pin(RELAY_OUT6, Pin.OUT)

#led = Pin(LED_PIN, Pin.OUT)
#led.off()  # Stäng av LED-lampan initialt

relay_out1.off()
relay_out2.off()
relay_out3.off()
relay_out4.off()
relay_out5.off()
relay_out6.off()

# MQTT-inställningar
mqtt_server = '10.10.10.1'  # Anpassa med din MQTT-serveradress
client_id = 'PicoMQTTClient'
topic_sub = 'led_control'
topic_pub = 'led_status'

# Användarnamn och lösenord för MQTT-autentisering (om det behövs)
username = 'anton'
password = 'Lv98rsk7'

# Skapa en MQTT-klient och anslut till servern
client = MQTTClient(client_id, mqtt_server, user=username, password=password)
client.connect()


# Callback-funktion som körs när ett meddelande mottas
def message_callback(topic, msg):
    message = msg.decode('utf-8')
    print("Received message:", message)
    
    #relä 1
    
    if message == 'el_switch1_on':
        send_to_mqtt_on(relay_out1)
    elif message == 'el_switch1_off':
        send_to_mqtt_off(relay_out1)
        
    elif message == 'el_switch2_on':
        send_to_mqtt_on(relay_out2)
    elif message == 'el_switch2_off':
        send_to_mqtt_off(relay_out2)
        
    elif message == 'el_switch3_on':
        send_to_mqtt_on(relay_out3)
    elif message == 'el_switch3_off':
        send_to_mqtt_off(relay_out3)

    elif message == 'el_switch4_on':
        send_to_mqtt_on(relay_out4)
    elif message == 'el_switch4_off':
        send_to_mqtt_off(relay_out4)
        
    elif message == 'el_switch5_on':
        send_to_mqtt_on(relay_out5)
    elif message == 'el_switch5_off':
        send_to_mqtt_off(relay_out5)

    elif message == 'el_switch6_on':
        send_to_mqtt_on(relay_out6)
    elif message == 'el_switch6_off':
        send_to_mqtt_off(relay_out6)
    
    
def send_to_mqtt_on(relay_name):
    relay_name.on()
    print(str(relay_name) + " on")
    client.publish(topic_pub, str(relay_name) + "on")
    
def send_to_mqtt_off(relay_name):
    relay_name.off()
    print(str(relay_name) + " off")
    client.publish(topic_pub, str(relay_name) + "off")


# Prenumerera på det ämne där styrmeddelandena kommer att skickas
client.set_callback(message_callback)
client.subscribe(topic_sub)


# Huvudloopen
while True:
    try:
        client.check_msg()
        time.sleep(0.1)
    except OSError as e:
        print("Error:", e)
        break

client.disconnect()

