# YOU NEED TO IMPORT SOME OTHER LIBARYS FOR THIS

import network
import time
from machine import Pin
from umqtt.simple import MQTTClient
from machine import ADC, Pin
from dht11 import DHT11, InvalidChecksum
import onewire, ds18x20, time


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("open_plotter", "password_for_wifi")
time.sleep(5)
print(wlan.isconnected())
print(wlan.ifconfig())

adc = machine.ADC(4)
LED = machine.Pin("LED", machine.Pin.OUT)
pin = machine.Pin(28, Pin.OUT, Pin.PULL_DOWN)
sensor = DHT11(pin)

ow1 = onewire.OneWire(machine.Pin(2))  # Anslutning för första sensorn
ow2 = onewire.OneWire(machine.Pin(21))  # Anslutning för andra sensorn
ow3 = onewire.OneWire(machine.Pin(1))  # Anslutning för andra sensorn

temp_sensor1 = ds18x20.DS18X20(ow1)  # Första sensorn
temp_sensor2 = ds18x20.DS18X20(ow2)  # Andra sensorn
temp_sensor3 = ds18x20.DS18X20(ow3)  # Andra sensorn

devices1 = temp_sensor1.scan()  # Upptäckta enheter för första sensorn
devices2 = temp_sensor2.scan()  # Upptäckta enheter för andra sensorn
devices3 = temp_sensor3.scan()  # Upptäckta enheter för andra sensorn

#Topic in this case will be hello
topic_pub = 'hello'
topic_send = 'temp_pico'

# Setup for the mqqt broker
mqtt_server = ''
client_id = ''
user_t = ''
password_t = ''

last_message = 0
message_interval = 5
counter = 0

# the following will set the seconds between 2 keep alive messages
keep_alive = 5

#MQTT connect
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, user=user_t, password=password_t, keepalive=60)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

#reconnect & reset
def reconnect():
    print('Failed to connected to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

# This code is executed once a new message is published
def new_message_callback(topic, msg):
    topic , msg=topic.decode('ascii') , msg.decode('ascii')
    print("Topic: "+topic+" | Message: "+msg)

try:
    client = mqtt_connect()
    client.set_callback(new_message_callback)
    client.subscribe(topic_pub.encode('utf-8'))

except OSError as e:
    reconnect()

last_message = time.time()
# Main loop
while True:
    try:
        temp_sensor1.convert_temp()  # Konvertera temperatur för första sensorn
        temp_sensor2.convert_temp()  # Konvertera temperatur för andra sensorn
        temp_sensor3.convert_temp()  # Konvertera temperatur för andra sensorn
        
        time.sleep_ms(2000)  # Vänta på konvertering

        # Läs av temperaturvärden från första sensorn
        for device in devices1:
            temp = temp_sensor1.read_temp(device)
            print("Temperatur 1: {:.2f} °C".format(temp))
            client.publish("temp_motor", str(temp))

        # Läs av temperaturvärden från andra sensorn
        for device in devices2:
            temp = temp_sensor2.read_temp(device)
            print("Temperatur 2: {:.2f} °C".format(temp))
            client.publish("temp_olja", str(temp))
        
        for device in devices3:
            temp = temp_sensor3.read_temp(device)
            print("Temperatur3 : {:.2f} °C".format(temp))
            client.publish("temp_avgas", str(temp))

        client.check_msg()
        time.sleep(0.0001)
        if (time.time() - last_message) > keep_alive:
            ADC_voltage = adc.read_u16() * (3.3 / 65535)
            temperature_celsius = 27 - (ADC_voltage - 0.706) / 0.001721
            temp_fahrenheit = 32 + (1.8 * temperature_celsius)
            client.publish(topic_send, str(round(temperature_celsius, 1)))
            last_message = time.time()
            print("send message")
            t = sensor.temperature
            h = sensor.humidity
            sensor.measure()
            client.publish("temp_motorrum", str(sensor.temperature))
            client.publish("hum_motorrum", str(sensor.humidity))

    except OSError as e:
        print(e)
        reconnect()
        pass

client.disconnect()

