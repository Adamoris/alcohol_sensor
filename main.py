import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time
import firebase
import json

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create an analog input channel on pin 0
chan = AnalogIn(ads, ADS.P0)

# MiCS-5524 Alcohol Detection
# Conversion factor from sensor to ppm determind through calibration
CONVERSION_FACTOR = 0.1

# Ethanol ppm thresholds
THRESHOLD_LOW = 10
THRESHOLD_HIGH = 500

# login to firebase
with open('account.json') as f:
    account = json.load(f)

firebase.login(account['email'], account['password'])
user = firebase.auth.current_user
print(user)

# Continuously display the reading and voltage
while True:
    print(f"Analog Value: {chan.value}, Voltage: {chan.voltage}")
    raw_value = chan.value
    ethanol_ppm = raw_value * CONVERSION_FACTOR
    print(f"Ethanol PPM: {ethanol_ppm}")

    if THRESHOLD_LOW <= ethanol_ppm <= THRESHOLD_HIGH:
        print("Alcohol Detected!")

        # Check if user's alcohol_detected field is already True
        value = firebase.read_from_firebase()

        if not value:
            # Write to Firebase at users/{user['localId']}/alcohol_detected
            data = {
                "alcohol_detected": True,
            }
            firebase.write_to_firebase(data)
    else:
        print("No Alcohol Detected")
        
    time.sleep(1.0)