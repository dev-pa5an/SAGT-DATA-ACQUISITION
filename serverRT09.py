import sys
sys.path.insert(0, "..")
import time
import random
from opcua import ua, Server

if __name__ == "__main__":

    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840")

    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    objects = server.get_objects_node()
    crane_data = objects.add_object(idx, "CraneData")  # Object to hold the tags

    # Create the tags
    hoist_hours = crane_data.add_variable(idx, "hoist_hours", 0)
    trolley_hours = crane_data.add_variable(idx, "trolley_hours", 0)
    gantry_hours = crane_data.add_variable(idx, "gantry_hours", 0)
    control_on = crane_data.add_variable(idx, "control_on", False)

    # Make tags writable (optional)
    hoist_hours.set_writable()
    trolley_hours.set_writable()
    gantry_hours.set_writable()
    control_on.set_writable()

    server.start()

    try:
        while True:
            time.sleep(5)  # Update every 5 seconds (adjust as needed)

            # Generate random values (adjust ranges as needed)
            hoist_hours.set_value(hoist_hours.get_value() + random.uniform(0.5, 2.0)) 
            trolley_hours.set_value(trolley_hours.get_value() + random.uniform(0.3, 1.5))
            gantry_hours.set_value(gantry_hours.get_value() + random.uniform(0.1, 0.8))
            control_on.set_value(random.choice([True, False]))

    finally:
        server.stop()