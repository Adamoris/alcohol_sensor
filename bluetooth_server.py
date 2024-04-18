import asyncio
from bleak import BleakServer

# Define UUIDs for the service and a writable characteristic
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHARACTERISTIC_UUID = "12345678-1234-5678-1234-56789abcdef1"

def callback_handler(sender, data):
    """
    Handle data written to the characteristic
    :param sender: the characteristic on which data was written
    :param data: the data received (bytes)
    """
    received_string = data.decode('utf-8')
    print(f"Received data: {received_string}")
    # Here you can add code to process the received data and potentially send a response
    return b"Received your message: " + data  # Echo back the received data for demonstration

async def main():
    async with BleakServer() as server:
        # Add a service and a characteristic to the server
        service = await server.add_new_service(SERVICE_UUID)
        await service.add_new_characteristic(CHARACTERISTIC_UUID, ["write"], callback=callback_handler)
        
        print(f"Service UUID: {SERVICE_UUID}")
        print(f"Characteristic UUID: {CHARACTERISTIC_UUID}")

        # Start advertising the service
        await server.start_advertising()

        try:
            while True:
                await asyncio.sleep(1)  # Keep the server running
        except KeyboardInterrupt:
            await server.stop_advertising()
            print("Server has stopped advertising.")

if __name__ == "__main__":
    asyncio.run(main())
