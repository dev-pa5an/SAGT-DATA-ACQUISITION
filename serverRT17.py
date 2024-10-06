import sys
sys.path.insert(0, "..")
import time
import random
from opcua import ua, Server

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run a simulated crane OPC UA server.")
    parser.add_argument("crane_id", type=str, help="Unique ID for this crane (e.g., 'Crane1')")
    parser.add_argument("--port", type=int, default=4840, help="Port for the OPC UA server (default: 4840)")
    args = parser.parse_args()

    server = Server()
    endpoint = f"opc.tcp://0.0.0.0:{args.port}"
    server.set_endpoint(endpoint)
    
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    objects = server.get_objects_node()
    crane_data = objects.add_object(idx, "RT17")  # Object node name is "RT17"

    # Variables under "RT17"
    hoist_hours = crane_data.add_variable(idx, "hoist_hours", 0, ua.VariantType.Double)
    trolley_hours = crane_data.add_variable(idx, "trolley_hours", 0, ua.VariantType.Double)
    gantry_hours = crane_data.add_variable(idx, "gantry_hours", 0, ua.VariantType.Double)
    control_on = crane_data.add_variable(idx, "control_on", False, ua.VariantType.Boolean)


    # uri = "RT17"
    # idx = server.register_namespace(uri)

    # objects = server.get_objects_node()
    # crane_data = objects.add_object(idx, f"{args.crane_id}Data")

    # # Create the tags with data types
    # hoist_hours = crane_data.add_variable(idx, "hoist_hours", 0, ua.VariantType.Double)
    # trolley_hours = crane_data.add_variable(idx, "trolley_hours", 0, ua.VariantType.Double)
    # gantry_hours = crane_data.add_variable(idx, "gantry_hours", 0, ua.VariantType.Double)
    # control_on = crane_data.add_variable(idx, "control_on", False, ua.VariantType.Boolean)

    # Make tags writable (optional)
    hoist_hours.set_writable()
    trolley_hours.set_writable()
    gantry_hours.set_writable()
    control_on.set_writable()

    print(f"Starting {args.crane_id} server on {endpoint}")
    print(f"Namespace index for {uri}: {idx}")

    server.start()

    try:
        while True:
            time.sleep(5)
            hoist_hours.set_value(hoist_hours.get_value() + random.uniform(0.5, 2.0)) 
            trolley_hours.set_value(trolley_hours.get_value() + random.uniform(0.3, 1.5))
            gantry_hours.set_value(gantry_hours.get_value() + random.uniform(0.1, 0.8))
            control_on.set_value(random.choice([True, False]))

            # More informative print statement
            # print(f"{args.crane_id} - Hoist: {hoist_hours.get_value():.2f}, Trolley: {trolley_hours.get_value():.2f}, "
            #       f"Gantry: {gantry_hours.get_value():.2f}, Control: {control_on.get_value()}") 

    finally:
        server.stop()