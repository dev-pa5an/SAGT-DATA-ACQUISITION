import asyncio
import time
from asyncua import Client

async def main():
    url = "opc.tcp://localhost:4840/freeopcua/server/" 
    async with Client(url=url) as client:
        while True:
            try:
                # Get the node you want to read from
                node = client.get_node("ns=2;i=85") # Correct namespace if needed

                # Read the value
                value = await node.read_value()
                print(f"Value: {value} @ {time.strftime('%H:%M:%S')}")

                # --- Do something with the 'value' --- 
                # Example: Send it over a network, update a database, etc.
                # ...

                # Wait for a specific duration
                await asyncio.sleep(1)  # Read every 1 second (adjust as needed)

            except Exception as e:
                print(f"Error: {e}")
                await asyncio.sleep(2)  # Wait before retrying

if __name__ == "__main__":
    asyncio.run(main())