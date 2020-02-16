import Adafruit_DHT as dht
import time
import requests
import json

while True:
    time.sleep(1)
    h,t = dht.read_retry(dht.DHT22, 4)  # 这里的4对应着 GPIO#4
    payload = {'temperature': '{0:0.2f}'.format(t), 'humidity': '{0:0.2f}'.format(h)}
    requests.post("http://192.168.0.103/temp/data", data=payload)