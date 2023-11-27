# HomeSecurity_IOT

## Overview
This Python script is designed for a Raspberry Pi to capture images from a connected camera, send the images via email, and publish them to an MQTT topic. It also includes functionality to control an LED based on MQTT messages. The script is configured to connect to the broker.emqx.io MQTT broker.

## Dependencies
- Python 3
- OpenCV (`pip install opencv-python`)
- Paho MQTT (`pip install paho-mqtt`)

## Configuration
- Ensure the necessary dependencies are installed.
- Set up the GPIO pins for the LED and switch according to the script.
- Configure the MQTT broker URL in the script or as an environment variable.
- Update the email configuration with sender and recipient email addresses and password.

## Usage
1. Run the script on the Raspberry Pi.
2. Press the physical switch connected to GPIO pin 17 to capture an image, send it via email, and publish it to the "image.jpg" MQTT topic.
3. Monitor the LED to indicate the state of the device based on MQTT messages.

## Notes
- Ensure the camera is properly connected and configured on the Raspberry Pi.
- Customize email and MQTT configurations according to your setup.
- Handle potential security considerations, such as securing email password and MQTT communication.

## Author
IRSHAAD ABDUL GAFOOR KHAN ABDUL SAMADU
