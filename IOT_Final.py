import RPi.GPIO as GPIO
import cv2, smtplib
import paho.mqtt.publish as publish
import time,os,sys
from time import sleep
from urllib.parse import urlparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
LED_PIN=11 
GPIO.setup(LED_PIN,GPIO.OUT)  
url_str = os.environ.get('CLOUDMQTT_URL', 'tcp://broker.emqx.io:1883') 
url = urlparse(url_str)
mqttc.connect(url.hostname, url.port)
rc = 0
while True:
    while rc == 0:
        import time   
        rc = mqttc.loop()
    print("rc: " + str(rc))
    
GPIO.setmode(GPIO.BCM)
switch_pin = 17
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
mqttc = paho.Client()                       
mqttc.on_message = on_message                          
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Email configuration
sender_email = "deepakpanth413@gmail.com"
recipient_email = "deepakpanth413@gmail.com"
email_password = "*******"

def on_connect(self, mosq, obj, rc):
        self.subscribe("led", 0)
        
def on_message(mosq, obj, msg):
    print("test" + " " +str(msg.payload))
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    if msg.payload == b'on':    
        print ("LED on")     
        GPIO.output(LED_PIN,GPIO.HIGH)  #LED ON
    else:    
        print ("LED off")
        GPIO.output(LED_PIN,GPIO.LOW)   # LED OFF   
        
def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))
    
def send_email(image_path):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = "Picture from Raspberry Pi"

    # Attach the image to the email
    with open(image_path, "rb") as img_file:
        image = MIMEImage(img_file.read(), name="image.jpg")
        msg.attach(image)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, email_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

def capture_and_send():
    image_path = "/home/pi/Downoads/image.jpg"  
    cap = cv2.VideoCapture(0)  
    ret, frame = cap.read()
    cv2.imwrite(image_path, frame)
    cap.release()
    send_email(image_path)

try:
    print("Press the switch to capture and send an image")
    while True:
        switch_state = GPIO.input(switch_pin)
        if switch_state == GPIO.LOW:
            print("Switch is pressed. Capturing and sending an image...")
	    bytar = bytearray('image.jpg',"rb")
	    publish.single('image.jpg',bytar , qos = 1 , hostname='broker.emqx.io')
            capture_and_send()
            time.sleep(5)  # Wait for a while to avoid rapid image capture

except KeyboardInterrupt:
    print("\nProgram terminated by user")

finally:
    GPIO.cleanup()
    print("GPIO cleanup complete")