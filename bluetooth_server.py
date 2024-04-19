import asyncio
from bless import BlessServer, BlessGATTCharacteristic, GATTCharacteristicProperties, GATTAttributePermissions

# Define your service and characteristic UUIDs
service_uuid = "12345678-1234-5678-1234-56789abcdef0"
char_uuid = "12345678-1234-5678-1234-56789abcdef1"

# Define the BLE server
class SimpleBleServer:
    def __init__(self, loop):
        # Create the server instance
        self.server = BlessServer(name="TestBLEServer", loop=loop)
        self.loop = loop
        self.characteristic = None

    async def setup_ble(self):
        # Add a new service
        await self.server.add_new_service(service_uuid)

        # Define properties and permissions for the characteristic
        char_properties = GATTCharacteristicProperties.read | GATTCharacteristicProperties.write
        char_permissions = GATTAttributePermissions.readable | GATTAttributePermissions.writeable

        # Add a new characteristic
        self.characteristic = BlessGATTCharacteristic(
            uuid=char_uuid,
            properties=char_properties,
            permissions=char_permissions,
            value=[]
        )
        
        # Attach the characteristic to the service
        await self.server.add_new_characteristic(service_uuid, self.characteristic)
        
        # Define callbacks
        self.characteristic.set_write_callback(self.on_write)
        
    async def start_server(self):
        # Start advertising the BLE service
        await self.server.start()
        print("Server started and advertising...")
        
    def on_write(self, value, options):
        # Handle write requests
        message = bytes(value).decode('utf-8')
        print(f"Received message: {message}")
        # Optionally process the message and respond (echo back for simplicity)
        return value  # Echo back the same message for confirmation

# Run the server
async def main():
    loop = asyncio.get_event_loop()
    ble_server = SimpleBleServer(loop)
    await ble_server.setup_ble()
    await ble_server.start_server()
    await asyncio.Future()  # Run forever

if __name__ == '__main__':
    asyncio.run(main())
