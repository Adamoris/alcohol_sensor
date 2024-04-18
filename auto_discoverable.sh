#!/bin/bash

# Check if Bluetooth is connected by looking for connected devices
if bluetoothctl info | grep -q "Connected: yes"; then
    echo "A device is connected."
else
    echo "No devices connected. Making the device discoverable."
    # Make the device discoverable
    bluetoothctl discoverable on
    # Optionally set discoverable timeout (0 means always discoverable)
    bluetoothctl discoverable-timeout 0
fi

