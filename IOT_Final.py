import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import paho.mqtt.publish as publish
import paho.mqtt.client as paho
import time
import cv2
import os,sys
import RPi.GPIO as GPIO
import urlparse

def accesspart():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    LED_PIN=23 
    GPIO.setup(LED_PIN,GPIO.OUT)   # Set pin function as output
    
    def on_connect(self, mosq, obj, rc):
            self.subscribe("led", 0)
        
    def on_message(mosq, obj, msg):
        print("Check in the MQTT Dashboard to give access!")
        if msg.payload == b'on':    
            print ("Access granted")     
            GPIO.output(LED_PIN,GPIO.HIGH)  #LED ON
        else:    
            print ("Access denied")
            GPIO.output(LED_PIN,GPIO.LOW)   # LED OFF
            exit()
            #return
    
    def on_publish(mosq, obj, mid):
        print("mid: " + str(mid))
        
    def on_subscribe(mosq, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))
    
    mqttc = paho.Client()                        
    mqttc.on_message = on_message                
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    url_str = os.environ.get('CLOUDMQTT_URL', 'tcp://broker.emqx.io:1883') 
    url = urlparse.urlparse(url_str)
    mqttc.connect(url.hostname, url.port)
    
    rc = 0
    
    while True:
        while rc == 0:
            rc = mqttc.loop()
            time.sleep(0.5)
        return
    exit()
def bellpart():
    #rc = 0
    # Set GPIO mode and pin
    GPIO.setmode(GPIO.BCM)
    switch_pin = 17
    flag = 0
    # Setup the switch pin as input with a pull-up resistor
    GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    try:
        print("Press the switch to see the state")
        while True:
            # Read the state of the switch
            switch_state = GPIO.input(switch_pin)
    
            # Check if the switch is pressed (LOW state due to pull-up resistor)
            if switch_state == GPIO.LOW:
                print("Switch is pressed")
                emailpart()
                mqttpart(flag)
                accesspart()
            else:
                print("Switch is not pressed")
            # Wait for a short duration to avoid rapid state changes
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\nProgram END")

def emailpart():
    print('Executing Email Part Now')
    subprocess.call(['fswebcam', 'image.jpg'])
    print('Image Captured')
    print('Sending the captured image to mail')
    email_sender = 'deepakpanth413@gmail.com'
    email_receiver = 'deepakpanth413@gmail.com'
    subject = 'User asking for access'
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject']= subject
    body = 'This person is waiting outside'
    msg.attach(MIMEText(body, 'plain'))
    
    with open("image.jpg", "rb") as img_file:
        img_data = img_file.read()
        image = MIMEImage(img_data, name="image.jpg")
        msg.attach(image)
    
    text = msg.as_string()
    connection = smtplib.SMTP('smtp.gmail.com', 587)
    connection.starttls()
    connection.login(email_sender, 'mfzbmqogktcdwwbj')
    connection.sendmail(email_sender, email_receiver, text )
    connection.quit()
    print('mail sent')
    
def mqttpart(flag):
    cam_port = 0
    video_capture = cv2.VideoCapture(cam_port)
    while(flag == 0):
     # reading the input using the camera
     result, image = video_capture.read()
     # saving image in local storage
     cv2.imwrite("Live_Image.jpg", image)
     f=open("Live_Image.jpg","rb")
     filecontent = f.read()
     byteArr = bytearray(filecontent)
     print("Sending the captured image to MQTT Dashboard")
     
     publish.single('image', byteArr, qos = 1, hostname='broker.emqx.io')
     
     time.sleep(0.2)
     print("Please check now in the application")
     flag = flag+1
     
     #cv2.imshow('Live_Image.png', image)
     #if (cv2.waitKey(2) == 27):
        #cv2.destroyAllWindows()
        #break
    
    video_capture.release()
    
    cv2.destroyAllWindows()

bellpart()


