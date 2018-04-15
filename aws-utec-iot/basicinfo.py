from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

import rospy
from std_msgs.msg import String
from avalos_intera.msg import robot_q


AllowedActions = ['both', 'publish', 'subscribe']


class SendIOT:
    def __init__(self):
        host = "a2ujlqua2mmq82.iot.us-west-2.amazonaws.com" #args.host
        rootCAPath = "root-CA.crt"
        certificatePath = "prueba_python.cert.pem"
        privateKeyPath = "prueba_python.private.key"
        useWebsocket = False
        clientId = "JoseAvalos_PubSub"
        topic = "data/q"
        mode="publish" #"-m", "--mode", action="store", dest="mode", default="both",

        # Init AWSIoTMQTTClient
        myAWSIoTMQTTClient = None
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
        myAWSIoTMQTTClient.configureEndpoint(host, 8883)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

        # AWSIoTMQTTClient connection configuration
        myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

        myAWSIoTMQTTClient.connect()


        self.pub_msg=[0,0,0,0,0,0,0,0]
        #rospy.Subscriber("avalos/iot/values_q", robot_q, self.sender)

        if mode == 'both' or mode == 'subscribe':
            myAWSIoTMQTTClient.subscribe(topic, 1, self.customCallback)
            time.sleep(0.05)
        while True: #not rospy.is_shutdown():
            if mode == 'both' or mode == 'publish':
                message = {}
                message['head'] = 0.1#self.pub_msg[0]
                message['right_j0'] = 0.2#self.pub_msg[1]
                message['right_j1'] = 0.3#self.pub_msg[2]
                message['right_j2'] = 0.4#self.pub_msg[3]
                message['right_j3'] = 0.5#self.pub_msg[4]
                message['right_j4'] = 0.6#self.pub_msg[5]
                message['right_j5'] = 0.7#self.pub_msg[6]
                message['right_j6'] = 0.8#self.pub_msg[7]
                messageJson = json.dumps(message)
                myAWSIoTMQTTClient.publish(topic, messageJson, 1)

    # Custom MQTT message callback
    def customCallback(client, userdata, message):
    #    print(message.topic)
        print("recived msg\n")

    def sender(self,d): 
        self.pub_msg=d.angle

if __name__ == '__main__':
       
    send=SendIOT()
    print("begin send... ")
