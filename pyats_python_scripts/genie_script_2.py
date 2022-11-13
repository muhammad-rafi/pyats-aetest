from genie.testbed import load
from rich import print as rprint
from unicon.core.errors import SubCommandFailure 

testbed_file = "testbed.yml"
testbed = load(testbed_file)

# print the testbed in Python dictionary
# rprint(testbed.__dict__['raw_config'])

device = testbed.devices['csr1000v-1']
# device.connect(log_stdout=False)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Connect to the device and run the raw cli commands 

# # Parameters dictionary for connect() 
# conn_param = {'learn_hostname': True, 
#               'learn_os': True, 
#               'init_config_commands': [], 
#               'init_exec_commands': ['terminal length 0', 
#                                      'show version',
#                                      'show ip interface brief'],
#               'log_stdout': 'False'
#               } 

# rprint(device.connect(**conn_param))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Another way to connect to the device and run the raw cli commands 

# List of command 
cmd_list = ['show version', 
            'show platform',
            'show ip interface brief',
            'show banner motd']

# Connect to the testbed device
output = device.connect(learn_hostname=True,
                        learn_os=True,
                        init_config_commands=[],
                        init_exec_commands=cmd_list,
                        log_stdout=False)
# print the output 
rprint(output)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
