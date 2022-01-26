import paho.mqtt.client as mqtt

#get unique cpu id of raspberry pi
def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"
    return cpuserial

#username = 'your user name'
username = 'jjy000'
#pwd = 'your password'
pwd = 'qazwsxedc123'
#broker = "your broker"
broker = "mqtt.arduino-hannover.de"
port = 1883
keepalive = 60
#topic = 'your topic'
seriel = getserial()
topic_command = 'jjy000/'+ seriel + '/command'
topic_data = 'jjy000/'+ seriel + '/data'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[INFO]Connected success")
        client.publish('jjy000/reportID', seriel+' connected successfully')
        client.subscribe(topic_command)
    else:
        print(f"[ERROR]Connected fail with code {rc}")

def on_message(client, userdata, msg):
    if (msg.topic == topic_command) & (msg.payload == b'submit_data'):
        print('[INFO]got the command to submit data')
        f = open("logs.csv", "rb")
        fileContent = f.read()
        byteArr = bytearray(fileContent)
        client.publish(topic_data, b'csv file will be sent!')
        client.publish(topic_data, byteArr)
        print(f"[INFO]data sent to {topic_data}")

client = mqtt.Client()
client.username_pw_set(username, pwd)
client.on_connect = on_connect
client.on_message = on_message
client.will_set( ('jjy000/' + seriel + '/status'),  b'{"status": "Off"}')
client.connect(broker, port, keepalive)
client.loop_forever()