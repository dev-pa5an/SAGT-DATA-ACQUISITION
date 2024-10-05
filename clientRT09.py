# import sys
# sys.path.insert(0, "../..")


# from asyncua.sync import Client, ua

from opcua import Client, ua

def read_input_value(node_id):
    client_node = client.get_node(node_id)
    client_node_value = client_node.get_value()
    
    print(client_node_value)

if __name__ == "__main__":
    
    client = Client("opc.tcp://0.0.0.0:4840")
    
    try:
        client.connect()
        root = client.get_root_node()
        print("Objects root node is ", root)
        
        read_input_value('ns=2;i=2')
        read_input_value('ns=2;i=3')
        read_input_value('ns=2;i=4')
    finally:
        client.disconnect()
    