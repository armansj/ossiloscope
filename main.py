import network
import socket
from machine import ADC, Pin
import time

ssid = 'Vodafone-820C'
password = 'xc5dadQYrqpo2J2sd2q2'

adc = ADC(Pin(26))


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        time.sleep(1)
    print('Connected to Wi-Fi:', wlan.ifconfig())


def send_data():
    address = ('192.168.0.41', 12345)

    s = socket.socket()
    s.connect(address)

    while True:
        adc_value = adc.read_u16()
        s.send(str(adc_value).encode())
        time.sleep(0.01)

    s.close()


# Main program
connect_wifi()
send_data()

