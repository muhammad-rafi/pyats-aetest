# from pyats.topology import loader 
from pyats.topology.loader import load


# Easy way to define the devices dictionary
testbed_dict = {'devices': {
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
                                'ip': 'sandbox-iosxe-latest-1.cisco.com'}
                                    }
                                }
                            }
                        }

# # To load the testbed from the Python dict defined above 
# # tb_dict = loader.load(testbed_dict) 
# tb_dict = load(testbed_dict) 
# print(type(tb_dict))

# To load the testbed from the 'testbed.yml' file exist in the current directory
# tb_file = loader.load('testbed.yml')
tb_file = load('testbed.yml')
print(type(tb_file))
