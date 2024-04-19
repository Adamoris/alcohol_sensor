import sys
import asyncio
from bless import BlessServer, BlessGATTCharacteristic, GATTCharacteristicProperties, GATTAttributePermissions

# Initialize server
async def run_server():
    server = BlessServer(name="MyBLEServer")
    
    # Define a service and characteristic UUID
    service_uuid = "12345678-1234-5678-1234-56789abcdef0"
    char_uuid = "12345678-1234-5678-1234-56789abcdef1"
    
    # Add service
    await server.add_new_service(service_uuid)
    
    # Define characteristic properties and permissions
    properties = GATTCharacteristicProperties.read | GATTCharacteristicProperties.write
    permissions = GATTAttributePermissions.readable | GATTAttributePermissions.writeable
    
    # Add characteristic
    await server.add_new_characteristic(
        service_uuid, char_uuid, properties, None, permissions,
        read_request_callback=read_request, write_request_callback=write_request
    )
    
    # Start server
    await server.start()
    print("BLE Server is running...")
    
    # Run server indefinitely
    await asyncio.Future()

def read_request(characteristic: BlessGATTCharacteristic, **kwargs):
    """Callback function to handle read requests."""
    print(f"Read request received: {characteristic.value}")
    return characteristic.value

def write_request(characteristic: BlessGATTCharacteristic, value, **kwargs):
    """Callback function to handle write requests."""
    print(f"Write request received: {value}")
    characteristic.value = value  # Echo back the value for demonstration

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_server())
