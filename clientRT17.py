from asyncua import Client, ua
import asyncio

async def read_crane_data(crane_id, server_url, node_id_base):
    async with Client(server_url) as client:
        print(f"Connected to {crane_id} server: {server_url}")
        while True:
            try:
                # Read tag values
                hoist_hours = await client.get_node(f"{node_id_base};i=2").read_value()
                trolley_hours = await client.get_node(f"{node_id_base};i=3").read_value()
                gantry_hours = await client.get_node(f"{node_id_base};i=4").read_value()
                control_on = await client.get_node(f"{node_id_base};i=5").read_value()

                # Print values
                print(f"{crane_id} - Hoist: {hoist_hours:.2f}, Trolley: {trolley_hours:.2f}, "
                      f"Gantry: {gantry_hours:.2f}, Control: {control_on}")

                await asyncio.sleep(5)  # Adjust update interval as needed

            except Exception as e:
                print(f"Error reading from {crane_id}: {e}")
                await asyncio.sleep(2)

async def main():
    crane_configs = [
        {"crane_id": "RT17", "server_url": "opc.tcp://localhost:4840", "node_id_base": "ns=2"}
    ]

    tasks = [read_crane_data(**config) for config in crane_configs]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
