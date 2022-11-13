from genie.testbed import load
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from rich import print as rprint

# This script using the testbed as json string define as dictionary

# # Easy wayto define the devices dictionary
# devices_dict = {"devices": {
#                     "csr1000v": {
#                         # "alias": "csr1000v-1",
#                         "ip": "sandbox-iosxe-latest-1.cisco.com",
#                         "port": 22,
#                         "protocol": "ssh",
#                         "username": "developer",
#                         "password": "C1sco12345",
#                         "os": "iosxe",
#                         }
#                     }
#                 }


# testbed = load(devices_dict)
# device=testbed.devices['csr1000v']
# device.connect()

# # Fetch the device username and password 
# print(device.api.get_username_password())

# Define testbed file in Python dictionary format 
testbed_devices = {
        'testbed': {'name': 'testbed for python sctipts', 
                    'testbed_file': 'testbed.yml'
                    },
        'devices': {
            'csr1000v-1': {
                'alias': 'csr1000v-1',
                'os': 'iosxe',
                'type': 'router',
                'platform': 'csr1000v',
                'credentials': {
                    'default': {
                        'username': 'developer', 
                        'password': 'C1sco12345'
                        }
                    },
                'connections': {
                    'vty': {
                        'protocol': 'ssh', 
                        'ip': 'sandbox-iosxe-latest-1.cisco.com'}}
            }
        },
        'topology': {}
    }

testbed = load(testbed_devices)
device = testbed.devices['csr1000v-1']
device.connect(log_stdout=False)

# # To loop over multiple devices defined in the testbed 
# testbed = load(testbed_devices)
# for device in testbed:
#     device.connect(learn_hostname=False,
#                    init_exec_commands=[],
#                    init_config_commands=[],
#                    log_stdout=True)
    
#     running_config = device.api.get_running_config()
#     print(running_config)

# To connect via Telnet - not recommended
# device.connect(via=vty, alias='vty')
# device.vty.execute('show version')
# device.mapping['cli'] = 'vty'

# # Get 'show version' in traditional CLI format 
# sh_version_exec = device.execute('show version')
# rprint(sh_version_exec)

# # Get 'show version' in parsed Python dict format  
# sh_version_parsed = device.parse('show version')
# rprint(sh_version_parsed)

# # To check what does pyats 'learn' feature offer 
# pyats_features = device.learn('all')
# for feature in pyats_features.keys():
#     rprint(feature)
    
# # Learn Interface on the device
# learnt_interfaces = device.learn('interface')
# for interface in learnt_interfaces.info:
#     rprint(interface)

# Parsed ping output from the device 
# try: 
#     parsed_ping = device.parse("ping 8.8.8.8")
#     print(parsed_ping) 
# except  SchemaEmptyParserError as e: 
#     print("There was an error") 

# is_connected

# Learn routing from the device
learn_routes = device.learn("routing")
print(learn_routes.info.keys())